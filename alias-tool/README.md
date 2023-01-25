# Alias Tool

This tool generates the `qemu_aliases` dictionary (or at least most of it) for Winbot/VMBot.

The aliases included with VMBot as of 2023-01-25 were generated with the host set to en-GB.
If you are using a VM with another keymap, such as `en-US`,
you may use this tool to generate a new set of aliases,
in order for symbol mapping (for `type` and `press` commands) to work correctly.

**TODO**: make Winbot load this from file