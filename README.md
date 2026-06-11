# Terminal Green - Standard Notes theme

A black-and-green Standard Notes theme inspired by old-school phosphor CRT terminals.

## Color palette

| Role | Color | Hex |
|---|---|---|
| Background | Black | `#000000` |
| Panels / sidebars | Dark green-tinted black | `#0a150a` |
| Primary text | Phosphor green | `#00ff41` |
| Secondary text | Dimmer green | `#00aa29` |
| Borders | Dark green | `#004400` |
| Warning | Chartreuse | `#aaff00` |
| Danger | Red (kept for visibility) | `#ff3333` |

Tag and folder tint colors follow ANSI terminal conventions (cyan, magenta, chartreuse, purple,
green, and amber), so color-coded tags remain distinguishable against the black background.

## Installation

1. Open Standard Notes and go to **Preferences -> Plugins -> Install Custom Plugin**.
2. Paste the raw CSS URL and confirm:

```
https://cdn.jsdelivr.net/gh/netromdk/sn-theme-terminal-green@master/ext.json
```

## Building from source

The source lives in `src/main.scss`. Compile it to `dist/dist.css` with:

```sh
./build.sh
```

The script requires `npm` (Node.js). On first run it installs `sass` locally into `node_modules/`
(no global install needed). Subsequent runs skip the install step.

To run the build step directly after `npm install`:

```sh
npm run build
```
