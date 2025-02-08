// For every option, see ~/.config/ags/modules/.configuration/user_options.js
// (vscode users ctrl+click this: file://./modules/.configuration/user_options.js)
// (vim users: `:vsp` to split window, move cursor to this path, press `gf`. `Ctrl-w` twice to switch between)
//   options listed in this file will override the default ones in the above file

const userConfigOptions = {
  'appearance': {
    'barRoundCorners': 0,
    'fakeScreenRounding': 0,
  },
  'time': {
    'format': "%I:%M %P",
  },
  'workspaces': {
        'shown': 5,
  },
  'icons': {
    'symbolicIconTheme':{
      "dark": "Papirus-Dark",
      "light": "Papirus-Light",
    },
    'substitutions': {
      'speech-dispatcher-dummy': 'transmageddon',
    },
  },
}

export default userConfigOptions;
