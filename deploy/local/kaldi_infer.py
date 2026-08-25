"""Live Kaldi transcription for one audio file, using the exported models/tri3/ model.

Reuses the exact recipe scaffold and decode invocation train_kaldi.ipynb builds
(path.sh/steps/utils symlinks, steps/make_mfcc.sh, steps/decode_fmllr.sh), just
scoped to a single ad-hoc utterance instead of the full test set. Must run on
Linux/WSL -- Kaldi doesn't build on native Windows (see CLAUDE.md).
"""

import os
import platform
import shlex
import shutil
import subprocess
import uuid
from pathlib import Path


def _q(path):
    # Paths under this repo (and WORK_DIR, by default) can contain spaces
    # (e.g. ".../Sugbodoc/speech model/...") -- always quote for the shell.
    return shlex.quote(str(path))

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
MODEL_DIR = Path(os.environ.get("BISAYA_KALDI_MODEL_DIR", PROJECT_ROOT / "models" / "tri3")).resolve()
KALDI_ROOT = Path(os.environ.get("KALDI_ROOT", Path.home() / "kaldi")).resolve()
# WSL-native by default (like train_kaldi.ipynb's WORK_DIR) -- old Kaldi shell
# scripts do unquoted path handling internally, so this must never sit on a
# /mnt/c path with spaces in it (this repo's own path has two: "windows 10",
# "speech model"). The model itself unavoidably lives under such a path, so
# _ensure_scaffold() below reaches it through a space-free symlink instead.
WORK_DIR = Path(os.environ.get("BISAYA_DEPLOY_WORK_DIR", Path.home() / "bisaya_deploy_work")).resolve()

# Fixed LM weight for decoding -- unlike evaluate_kaldi.ipynb, there's no
# reference transcript to sweep --min-lmwt/--max-lmwt against, so we just
# pick a fixed value from the middle of that notebook's swept range.
LMWT = int(os.environ.get("BISAYA_KALDI_LMWT", "13"))

REQUIRED_MODEL_FILES = [
    "final.mdl", "final.alimdl", "final.mat", "tree", "cmvn_opts", "splice_opts",
    "graph/HCLG.fst", "graph/words.txt",
]


def availability_status():
    """Returns (ready: bool, message: str)."""
    try:
        _check_environment()
        return True, f"models/tri3 found at {MODEL_DIR}"
    except RuntimeError as e:
        return False, str(e)


def _check_environment():
    if platform.system() != "Linux":
        raise RuntimeError(
            "Kaldi engine requires WSL2/Ubuntu or native Linux -- Kaldi doesn't "
            "build on native Windows. Run local_app.py with the WSL Python, not "
            "the Windows one (see deploy/README.md)."
        )
    if not (KALDI_ROOT / "src" / "featbin" / "compute-mfcc-feats").exists():
        raise RuntimeError(
            f"KALDI_ROOT={KALDI_ROOT} doesn't look like a built Kaldi checkout. "
            "Set the KALDI_ROOT env var to the same checkout train_kaldi.ipynb used."
        )
    missing = [f for f in REQUIRED_MODEL_FILES if not (MODEL_DIR / f).exists()]
    if missing:
        raise RuntimeError(
            f"{MODEL_DIR} is missing {missing} -- run train_kaldi.ipynb through "
            "its model-export stage first."
        )


def _sh(cmd, cwd):
    # ". ./path.sh &&" mirrors what every steps/*.sh script does internally;
    # prefixing it here too makes raw Kaldi binaries (lattice-best-path) work.
    full_cmd = f". ./path.sh && {cmd}"
    result = subprocess.run(
        full_cmd, shell=True, cwd=str(cwd), executable="/bin/bash",
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"command failed ({result.returncode}): {cmd}\n"
            f"--- stdout ---\n{result.stdout}\n--- stderr ---\n{result.stderr}"
        )
    return result.stdout


def _ensure_scaffold():
    WORK_DIR.mkdir(parents=True, exist_ok=True)

    path_sh = WORK_DIR / "path.sh"
    if not path_sh.exists():
        path_sh.write_text(
            "\n".join([
                f"export KALDI_ROOT={KALDI_ROOT}",
                "export PATH=$PWD/utils/:$KALDI_ROOT/tools/openfst/bin:$PWD:$PATH",
                ". $KALDI_ROOT/tools/config/common_path.sh",
                "export LC_ALL=C",
            ]) + "\n"
        )

    wsj_s5 = KALDI_ROOT / "egs" / "wsj" / "s5"
    for name in ("steps", "utils"):
        link = WORK_DIR / name
        if not link.exists():
            link.symlink_to(wsj_s5 / name)

    (WORK_DIR / "local").mkdir(exist_ok=True)
    score_sh = WORK_DIR / "local" / "score.sh"
    if not score_sh.exists():
        score_sh.symlink_to(Path("../steps/score_kaldi.sh"))

    (WORK_DIR / "conf").mkdir(exist_ok=True)
    mfcc_conf = WORK_DIR / "conf" / "mfcc.conf"
    if not mfcc_conf.exists():
        mfcc_conf.write_text("--use-energy=false\n")

    # Space-free path into models/tri3/ -- see the WORK_DIR comment above.
    model_link = WORK_DIR / "model"
    if not model_link.is_symlink():
        model_link.symlink_to(MODEL_DIR)


def transcribe(audio_path):
    """Transcribe one audio file with the exported Kaldi tri3 model. Returns text."""
    _check_environment()
    _ensure_scaffold()

    tag = uuid.uuid4().hex[:8]
    utt_id = f"deploy-{tag}"
    data_dir = WORK_DIR / "data" / f"infer_{tag}"
    mfcc_dir = WORK_DIR / "mfcc" / f"infer_{tag}"
    log_dir = WORK_DIR / "exp" / f"make_mfcc_infer_{tag}"
    model_link = WORK_DIR / "model"  # -> MODEL_DIR, created by _ensure_scaffold()
    decode_dir = model_link / f"decode_infer_{tag}"

    try:
        data_dir.mkdir(parents=True)
        (data_dir / "wav.scp").write_text(f'{utt_id} sox "{audio_path}" -r 16000 -c 1 -t wav - |\n')
        (data_dir / "utt2spk").write_text(f"{utt_id} {utt_id}\n")
        _sh(f"utils/utt2spk_to_spk2utt.pl {_q(data_dir)}/utt2spk > {_q(data_dir)}/spk2utt", cwd=WORK_DIR)

        _sh(f"steps/make_mfcc.sh --cmd run.pl --nj 1 {_q(data_dir)} {_q(log_dir)} {_q(mfcc_dir)}", cwd=WORK_DIR)
        _sh(f"steps/compute_cmvn_stats.sh {_q(data_dir)} {_q(log_dir)} {_q(mfcc_dir)}", cwd=WORK_DIR)
        _sh(f"utils/fix_data_dir.sh {_q(data_dir)}", cwd=WORK_DIR)

        graph_dir = model_link / "graph"
        _sh(
            f"steps/decode_fmllr.sh --cmd run.pl --nj 1 --skip-scoring true "
            f"{_q(graph_dir)} {_q(data_dir)} {_q(decode_dir)}",
            cwd=WORK_DIR,
        )

        ark_spec = f"ark:gunzip -c {decode_dir}/lat.1.gz|"
        out = _sh(
            f"lattice-best-path --lm-scale={LMWT} {_q(ark_spec)} ark,t:- "
            f"| utils/int2sym.pl -f 2- {_q(graph_dir)}/words.txt",
            cwd=WORK_DIR,
        )
        line = out.strip()
        return " ".join(line.split()[1:]) if line else ""
    finally:
        shutil.rmtree(data_dir, ignore_errors=True)
        shutil.rmtree(mfcc_dir, ignore_errors=True)
        shutil.rmtree(log_dir, ignore_errors=True)
        shutil.rmtree(decode_dir, ignore_errors=True)
        # decode_fmllr.sh's first-pass (pre-fMLLR) output -- a sibling dir
        # named "<decode_dir>.si", not a subdirectory of it.
        shutil.rmtree(f"{decode_dir}.si", ignore_errors=True)
