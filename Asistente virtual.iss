[Setup]
AppName=Asistente Virtual-Openai
AppVersion=1.0
DefaultDirName={pf}\Mi Aplicación Streamlit
OutputDir=c:\Users\Usuario
OutputBaseFilename=mi_aplicacion_setup

[Files]
Source: "C:\Users\Usuario\Asistente virtual-Openai\chat.py"; DestDir: "{app}"
Source:"C:\Users\Usuario\AppData\Local\Programs\Python\Python312\python.exe";DestDir: "{app}"
Source: "C:\Users\Usuario\Asistente virtual-Openai\style.css"; DestDir: "{app}"
Source: "C:\Users\Usuario\Asistente virtual-Openai\index.html"; DestDir: "{app}"
Source: "C:\Users\Usuario\Asistente virtual-Openai\requirements.txt"; DestDir: "{app}"
Source: "C:\Users\Usuario\Asistente virtual-Openai\.env"; DestDir: "{app}" 
Source: "C:\Users\Usuario\Asistente virtual-Openai\Logo Omardent.png"; DestDir: "{app}"
Source: "C:\Users\Usuario\Asistente virtual-Openai\Galatea D-ID.jpg"; DestDir: "{app}"
Source: "C:\Users\Usuario\Asistente virtual-Openai\.gitignore"; DestDir: "{app}" 
; ... (otras dependencias - cada archivo en una línea separada)

[Icons]
Name: "{group}\Asistente Virtual-Openai"; Filename: "{app}\chat.py"

[Run]
Filename: "{app}\python.exe"; Parameters: "streamlit run chat.py"