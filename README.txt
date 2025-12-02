<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Text Adventure Game Creator</title>
<style>
    body {
        font-family: Arial, sans-serif;
        margin: 40px;
        line-height: 1.6;
        background-color: #f7f7f7;
    }
    h1, h2 {
        color: #333;
        border-bottom: 2px solid #ccc;
        padding-bottom: 5px;
    }
    ul, ol {
        margin-left: 20px;
    }
    .section {
        background: #fff;
        padding: 20px;
        margin-bottom: 25px;
        border-radius: 8px;
        box-shadow: 0 0 5px rgba(0,0,0,0.1);
    }
    code {
        background: #eee;
        padding: 2px 4px;
        border-radius: 4px;
    }
</style>
</head>

<body>

<h1>TEXT ADVENTURE GAME CREATOR</h1>

<div class="section">
    <h2>Getting Started (Plug and Play)</h2>
    <ol>
        <li>Extract <code>TextGameCreator.zip</code> somewhere easily accessible.</li>
        <li>Run <code>editor/GameEditor.exe</code> to create or edit games.</li>
        <li>Use <strong>File &gt; New Game</strong> to create a new game.</li>
        <li>Build your world by adding rooms, items, enemies, and weapons.</li>
        <li>Save your game in the <code>data</code> folder.</li>
    </ol>
</div>

<div class="section">
    <h2>Playing a Game</h2>
    <ol>
        <li>Navigate to the <code>engine</code> folder in a terminal.</li>
        <li>Run <code>play.bat</code> (Windows).</li>
        <li>Enter the name of the game you want to play.</li>
        <li>Enjoy!</li>
    </ol>
</div>

<div class="section">
    <h2>Folder Structure</h2>
    <ul>
        <li><code>editor/</code> – Contains the game editor</li>
        <li><code>data/</code> – Your saved games go here</li>
        <li><code>engine/</code> – Contains the game engine</li>
    </ul>
</div>

<div class="section">
    <h2>How to Build the Project</h2>

    <h3>Requirements:</h3>
    <ul>
        <li>make</li>
        <li>g++ (version 17 or higher)</li>
        <li>python (version 3 or higher)</li>
    </ul>

    <h3>Instructions:</h3>
    <ol>
        <li>Make sure you have <code>make</code> installed and <code>g++</code> is in your PATH.</li>
        <li>Navigate to the root of the project directory.</li>
        <li>Run <code>make</code>.</li>
        <li>This will create <code>textgame.exe</code> with an example game.</li>
        <li>(Optional) To package the editor + engine for distribution, run <code>python package.py</code>.</li>
        <li>Navigate to <code>TextGameCreator</code> and run either the editor or engine.</li>
    </ol>

    <h3>Things to Note:</h3>
    <ul>
        <li>If .o files or the .exe aren’t being created, you may have the wrong version of g++.</li>
        <li><code>make clean</code> will not work unless the .exe already exists.</li>
        <li>The <code>TextGameCreator.zip</code> file is a full build that works independently.</li>
    </ul>
</div>

</body>
</html>
