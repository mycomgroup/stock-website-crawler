import { existsSync } from 'fs';
import { basename, dirname, join, resolve } from 'path';

const PROFILE_DIR_PATTERNS = [
  /^Default$/,
  /^Profile \d+$/,
  /^Guest Profile$/,
  /^System Profile$/
];

function stripWrappingQuotes(value) {
  return value.replace(/^['"`“”]+|['"`“”]+$/g, '');
}

function expandHome(value) {
  if (!value.startsWith('~/')) {
    return value;
  }

  const home = process.env.HOME;
  return home ? join(home, value.slice(2)) : value;
}

function looksLikeProfileDir(pathname) {
  const base = basename(pathname);
  if (PROFILE_DIR_PATTERNS.some((pattern) => pattern.test(base))) {
    return true;
  }

  return (
    existsSync(join(pathname, 'Preferences')) ||
    existsSync(join(pathname, 'Cookies')) ||
    existsSync(join(pathname, 'Network', 'Cookies'))
  );
}

function looksLikeUserDataDir(pathname) {
  return existsSync(join(pathname, 'Local State'));
}

export function resolveChromeProfile(useProfile) {
  if (!useProfile) {
    return null;
  }

  const sanitized = expandHome(stripWrappingQuotes(useProfile.trim()));
  const absolutePath = resolve(sanitized);

  if (!existsSync(absolutePath)) {
    throw new Error(
      `Chrome profile 路径不存在: ${absolutePath}\n` +
      '请传入真实的 Chrome 用户目录或具体 profile 目录，例如:\n' +
      '- /Users/你的用户名/Library/Application Support/Google/Chrome/Profile 5\n' +
      '- /Users/你的用户名/Library/Application Support/Google/Chrome/Default'
    );
  }

  if (looksLikeProfileDir(absolutePath)) {
    const profileDirectory = basename(absolutePath);
    return {
      originalPath: useProfile,
      inputPath: absolutePath,
      userDataDir: dirname(absolutePath),
      profileDirectory,
      launchArgs: [`--profile-directory=${profileDirectory}`]
    };
  }

  if (looksLikeUserDataDir(absolutePath)) {
    const defaultProfile = existsSync(join(absolutePath, 'Default')) ? 'Default' : null;
    return {
      originalPath: useProfile,
      inputPath: absolutePath,
      userDataDir: absolutePath,
      profileDirectory: defaultProfile,
      launchArgs: defaultProfile ? [`--profile-directory=${defaultProfile}`] : []
    };
  }

  throw new Error(
    `无法识别 Chrome profile 路径: ${absolutePath}\n` +
    '这个路径既不像 Chrome 用户目录，也不像具体的 profile 目录。'
  );
}

export function formatResolvedChromeProfile(profileConfig) {
  if (!profileConfig) {
    return '未指定';
  }

  if (!profileConfig.profileDirectory) {
    return profileConfig.userDataDir;
  }

  return `${profileConfig.userDataDir} (profile: ${profileConfig.profileDirectory})`;
}

export function enhanceChromeProfileError(error, profileConfig) {
  const message = error?.message || String(error);

  if (
    message.includes('user data directory is already in use') ||
    message.includes('ProcessSingleton') ||
    message.includes('SingletonLock')
  ) {
    return new Error(
      `Chrome profile 当前正在被其他 Chrome 进程占用，无法直接复用。\n` +
      `当前目标: ${formatResolvedChromeProfile(profileConfig)}\n` +
      '请先完全退出正在使用这个 profile 的 Chrome，再重新运行。'
    );
  }

  return error;
}
