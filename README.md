# password-manager

A local, encrypted CLI password vault. One master password (plus a secret iteration count) unlocks everything else — so you only ever have to remember two things.

Built to learn PBKDF2 key derivation and AES-GCM encryption hands-on, alongside coursework on AES/DES/RSA.

## How it works (short version)

- Your master password + a random salt get run through **PBKDF2HMAC** (480,000+ iterations recommended) to produce an encryption key.
- That key is used with **AES-GCM** to encrypt a JSON blob containing all your site/username/password entries.
- Everything (salt + nonce + encrypted data) is saved to one file: `vault.dat`.
- The **iteration count is never stored anywhere** — you type it in every time, same as the password. This makes it a second secret: even someone who knows your master password can't decrypt the vault without also knowing the exact iteration count.

## First-time setup (new machine)

```
git clone https://github.com/tetumer/password-manager.git
cd password-manager
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Every time after that (same machine, new terminal)

You only need to reactivate the environment — no need to reinstall anything:

```
cd password-manager
venv\Scripts\activate
python vault.py
```

## Using the tool

Run `python vault.py`. It will ask for:

1. **Master password** — hidden input, won't show on screen (this is normal, not broken).
2. **Iteration count** — the second secret. **Write this down somewhere safe outside this repo**, or you will lock yourself out of your own vault permanently.

Then you'll see a menu:

```
1. Add new entry
2. View an entry
3. List all sites
```

- **First time ever running this** (no `vault.dat` exists yet): you're setting a NEW master password and iteration count. Whatever you choose here becomes permanent — you cannot change them without decrypting and re-encrypting everything (not yet built).
- **Every time after**: you must enter the *exact same* master password and iteration count you used originally, or you'll get an `InvalidTag` error — this means wrong password, wrong iteration count, or both. There is no "forgot password" recovery. If you lose either secret, the vault is permanently unreadable.

## Important reminders (to future me)

- `vault.dat` contains your real encrypted passwords — it is `.gitignore`'d and must **never** be pushed to GitHub.
- The iteration count is not written down in the code or the file on purpose. If you forget it, nothing can recover your vault. Store it somewhere separate from this repo (not in your head only, ideally).
- `venv/` is also gitignored — always run `pip install -r requirements.txt` fresh on a new machine instead of expecting it to carry over.

## Known limitations (not yet built)

- No way to change master password or iteration count without manual re-encryption.
- No delete-entry option yet.
- No password generator yet (currently type your own password per entry).
- Wrong password/iteration count crashes with a raw Python traceback instead of a clean error message.
