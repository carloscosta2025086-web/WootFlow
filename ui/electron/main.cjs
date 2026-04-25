const { app, BrowserWindow, shell } = require("electron");
const path = require("path");
const { spawn } = require("child_process");

let mainWindow;
let pythonProcess;

const isDev = !app.isPackaged;
const PYTHON_PORT = 9120;
const VITE_PORT = 5173;

function startPythonServer() {
  const serverPath = path.join(__dirname, "..", "..", "server.py");
  const venvPython = path.join(
    __dirname,
    "..",
    "..",
    "..",
    ".venv",
    "Scripts",
    "python.exe"
  );

  const pythonCmd = require("fs").existsSync(venvPython)
    ? venvPython
    : "python";

  pythonProcess = spawn(pythonCmd, [serverPath], {
    cwd: path.join(__dirname, "..", ".."),
    stdio: ["pipe", "pipe", "pipe"],
  });

  pythonProcess.stdout.on("data", (data) => {
    console.log(`[Python] ${data.toString().trim()}`);
  });

  pythonProcess.stderr.on("data", (data) => {
    console.error(`[Python] ${data.toString().trim()}`);
  });

  pythonProcess.on("close", (code) => {
    console.log(`[Python] Process exited with code ${code}`);
  });
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1280,
    height: 820,
    minWidth: 960,
    minHeight: 640,
    frame: false,
    titleBarStyle: "hidden",
    titleBarOverlay: {
      color: "#0a0a0f",
      symbolColor: "#ffffff",
      height: 36,
    },
    backgroundColor: "#0a0a0f",
    webPreferences: {
      preload: path.join(__dirname, "preload.cjs"),
      contextIsolation: true,
      nodeIntegration: false,
    },
  });

  if (isDev) {
    mainWindow.loadURL(`http://localhost:${VITE_PORT}`);
    mainWindow.webContents.openDevTools({ mode: "detach" });
  } else {
    mainWindow.loadFile(path.join(__dirname, "..", "dist", "index.html"));
  }

  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url);
    return { action: "deny" };
  });
}

app.whenReady().then(() => {
  startPythonServer();

  // Give the Python server a moment to start
  setTimeout(createWindow, 1500);
});

app.on("window-all-closed", () => {
  if (pythonProcess) {
    pythonProcess.kill();
  }
  app.quit();
});

app.on("before-quit", () => {
  if (pythonProcess) {
    pythonProcess.kill();
  }
});
