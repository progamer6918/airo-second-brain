# WSL retirement acceptance gates

This procedure extends native Windows interface migration with staged validation before removing a local Linux environment.

## Daily Windows access

Use Windows-native applications and SSH. Back up configuration before disconnecting Linux network-drive mappings, hiding Linux terminal profiles or retiring Linux application shortcuts. Verify every shortcut target and indirect startup script; a native-looking shortcut can still invoke WSL.

## Native acceptance

Verify one relay instance, a fresh local capture without transmission, a Calculator launch, a disposable note create/read/delete through native Obsidian, and an authenticated restore-tested native backup. Verify the remote worker and gateway remain healthy. Application launch or queue completion alone does not prove every desktop actuator or manual editor interaction.

The Owner performs reboot manually after saving work. Repeat the native checks after login and observe normal Windows use for sixty minutes. Inspect both running distributions and the WSL VM. Accessing Linux folders during this observation invalidates the no-WSL acceptance gate.

## Whole-distro recovery

Require sufficient independent storage before export. Do not treat a mapped WSL drive as an independent backup or a selected-file archive as proof of complete distro recovery. Authenticate and restore the complete export into an isolated test distribution. Disable its application autostarts, networking, Windows interop and drive automount before running recovery checks. Preserve the original distribution and original export.

## Removal and rollback

Removal requires separate Owner approval after the evidence is reviewable. Unregister only the exact approved distributions and remove only the approved WSL components. Preserve shared virtualization features. After removal and a second manual reboot, repeat native acceptance, the sixty-minute observation and the next daily backup cycle. Retain the tested recovery archive and instructions; do not enable retired jobs during rollback.

Until all gates pass, report the remaining reboot, storage, restore, approval or removal work explicitly. Runtime migration and full WSL removal are separate completion claims.
