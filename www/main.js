$(document).ready(function () {
  $(".text").textillate({
    loop: true,
    sync: true,
    in: {
      effect: "bounceIn",
    },
    out: {
      effect: "bounceOut",
    },
  });

  //siri configuration
  var siriWave = new SiriWave({
    container: document.getElementById("siri-container"),
    width: 800,
    height: 200,
    style: "ios9",
    amplitude: "1",
    speed: "0.30",
    autostart: true,
  });

  //siri message annimation
  $(".siri-message").textillate({
    loop: true,
    sync: true,
    in: {
      effect: "fadeInUp",
      sync: true,
    },
    out: {
      effect: "fadeInOut",
      sync: true,
    },
  });

  //mic button click event

  $("#MicBtn").click(function () {
    console.log("Mic button clicked");
    eel.playAssistantsound();
    $("#Oval").attr("hidden", true);
    $("#SiriWave").attr("hidden", false);
    console.log("Calling eel.allCommands()");
    eel.allCommands()();
  });

  function doc_keyUp(e) {
    if (e.key === "j" && e.metaKey) {
      eel.playAssistantsound();
      $("#Oval").attr("hidden", true);
      $("#SiriWave").attr("hidden", false);
      eel.allCommands()();
    }
  }
  document.addEventListener("keyup", doc_keyUp, false);

  // to play assisatnt
  function playAssistant(message) {
    if (message != "") {
      $("#Oval").attr("hidden", true);
      $("#SiriWave").attr("hidden", false);
      eel.allCommands(message);
      $("#chatbox").val("");
      $("#MicBtn").attr("hidden", false);
      $("#SendBtn").attr("hidden", true);
    }
  }

  // toogle fucntion to hide and display mic and send button
  function ShowHideButton(message) {
    if (message.length == 0) {
      $("#MicBtn").attr("hidden", false);
      $("#SendBtn").attr("hidden", true);
    } else {
      $("#MicBtn").attr("hidden", true);
      $("#SendBtn").attr("hidden", false);
    }
  }

  // $("#chatbox").keyup(function () {
  //     let message = $("#chatbox").val();
  //     showHideButton(message)
  //   });
  // $("#SendBtn").click(function () {
  //     let message = $("#chatbox").val();
  //     playAssistant(message)
  //  });

  $("#chatbox").keypress(function (e) {
    key = e.which;
    if (key == 13) {
      let message = $("#chatbox").val();
      playAssistant(message);
    }
  });
});
const popupOverlay = document.getElementById("popupOverlay");
const popupCloseBtn = document.getElementById("popupCloseBtn");
const openPopupBtn = document.querySelector(".open-popup-btn");

// Open Popup
openPopupBtn.addEventListener("click", () => {
  popupOverlay.style.display = "flex";
});

// Close Popup on close button
popupCloseBtn.addEventListener("click", () => {
  popupOverlay.style.display = "none";
});

// // Close Popup if click outside the popup box
// popupOverlay.addEventListener("click", (event) => {
//   if (event.target === popupOverlay) {
//     popupOverlay.style.display = "none";
//   }
// });



const keywordInput = document.querySelector('.keyword-input');
const pathInput = document.querySelector('.path-input');
const addBtn = document.querySelector('.add-btn');
const commandTableBody = document.querySelector('.command-table tbody');

window.onload = loadCommands;

async function loadCommands() {
  const data = await eel.get_commands()();
  commandTableBody.innerHTML = '';
  data.forEach((cmd, index) => {
    const row = `
      <tr>
        <td>${index + 1}</td>
        <td>${cmd.name}</td>
        <td>${cmd.path}</td>
        <td><button class="delete-btn" onclick="deleteCommand(${cmd.rowid})">Delete</button></td>
      </tr>
    `;
    commandTableBody.innerHTML += row;
  });
}

addBtn.addEventListener('click', async () => {
  const keyword = keywordInput.value.trim();
  const path = pathInput.value.trim();
  if (!keyword || !path) {
    alert('Both fields are required');
    return;
  }

  const success = await eel.add_command(keyword, path)();
  if (success) {
    keywordInput.value = '';
    pathInput.value = '';
    loadCommands();
  } else {
    alert('Failed to add command');
  }
});

async function deleteCommand(id) {
  const success = await eel.delete_command(id)();
  if (success) {
    loadCommands();
  } else {
    alert('Failed to delete command');
  }
}

// Calls Python to stop speaking

// function stopSpeech() {
//   try {
//     eel.stopSpeaking()(); // <- Note the double parentheses to call the async exposed function
//     console.log("Speech stopped successfully.");
//   } catch (error) {
//     console.error("Error stopping speech:", error);
//   }
// }
