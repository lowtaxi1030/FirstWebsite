const searchButton = document.getElementById("search");

// 搜尋框
const playerIdInput = document.getElementById("player-id");
const playerNameInput = document.getElementById("player-name");

// 篩選區
const levelMinInput = document.getElementById("level-min");
const levelMaxInput = document.getElementById("level-max");
const scoreMinInput = document.getElementById("score-min");
const scoreMaxInput = document.getElementById("score-max");

// 篩選按鈕
const filterButton = document.getElementById("filter");

filterButton.addEventListener("click", function () {
  const playerId = playerIdInput.value;
  const playerName = playerNameInput.value;

  const levelMin =
    levelMinInput.value === "" ? null : Number(levelMinInput.value);
  const levelMax =
    levelMaxInput.value === "" ? null : Number(levelMaxInput.value);
  const scoreMin =
    scoreMinInput.value === "" ? null : Number(scoreMinInput.value);
  const scoreMax =
    scoreMaxInput.value === "" ? null : Number(scoreMaxInput.value);

  const levelReasonable = validateFilters(levelMin, levelMax);
  const scoreReasonable = validateFilters(scoreMin, scoreMax);

  if (!levelReasonable) {
    alert("等級篩選條件出錯！");
    return;
  }
  if (!scoreReasonable) {
    alert("分數篩選條件出錯！");
    return;
  }

  const filterParams = new URLSearchParams();
  if (levelMin !== null) {
    filterParams.set("min_level", levelMin);
  }
  if (levelMax !== null) {
    filterParams.set("max_level", levelMax);
  }
  if (scoreMin !== null) {
    filterParams.set("min_score", scoreMin);
  }
  if (scoreMax !== null) {
    filterParams.set("max_score", scoreMax);
  }
  filterParams.set("player_id", playerId);
  filterParams.set("player_name", playerName);
  const url = `/api/player?${filterParams.toString()}&mode=filter`;

  fetchPlayers(url);
});

function validateFilters(min, max) {
  if (min === null || max === null) {
    return true;
  }

  return min <= max;
}

//顯示搜尋結果
const resultArea = document.getElementById("result-area");

searchButton.addEventListener("click", function () {
  const playerId = playerIdInput.value;
  const playerName = playerNameInput.value;
  if (playerId.trim() === "" && playerName.trim() === "") {
    alert("請輸入玩家 ID 或玩家姓名！");
    return;
  }

  let url;

  if (playerId.trim() !== "") {
    url = `/api/player?player_id=${encodeURIComponent(playerId)}&mode=search`;
  } else {
    url = `/api/player?player_name=${encodeURIComponent(playerName)}&mode=search`;
  }

  fetchPlayers(url);
});

function fetchPlayers(url) {
  fetch(url)
    .then((response) => {
      if (!response.ok) {
        throw new Error("查無玩家");
      }
      return response.json();
    })
    .then((data) => {
      displayPlayers(data);
    })
    .catch((error) => {
      console.error("查詢玩家時發生錯誤:", error);
      alert("查詢玩家時發生錯誤：" + error.message);
    });
}

function displayPlayers(data) {
  // 使用取得的資料
  console.log(data);

  if (data.count === 1) {
    displayOneData(data.players[0]);
  } else if (data.count > 1) {
    displayMultipleData(data.players, data.count);
  } else {
    resultArea.innerHTML =
      "<h2>搜尋結果：查無玩家</h2><p class='hint2'>總共 0 位玩家</p>";
  }
}

function displayOneData(data) {
  resultArea.innerHTML = "<h2>搜尋結果</h2><p class='hint2'>總共 1 位玩家</p>"; // Clear previous results

  const playerDiv = createPlayerElement(data, 0);
  resultArea.appendChild(playerDiv);
}

function displayMultipleData(players, count) {
  // Implementation for displaying multiple player data
  resultArea.innerHTML =
    "<h2>搜尋結果</h2><p class='hint2'>總共 " + count + " 位玩家</p>"; // Clear previous results
  players.forEach((player, index) => {
    const playerDiv = createPlayerElement(player, index);
    resultArea.appendChild(playerDiv);
  });
}

function createPlayerElement(player, index) {
  const playerDiv = document.createElement("div");
  playerDiv.className = "player-card";
  playerDiv.innerHTML = `
    <h3>Player ${index + 1}</h3>
    <p>Player Name: ${player.name ?? "no data"}</p>
    <p>Player ID: ${player.player_id ?? "no data"}</p>
    <p>Level: ${player.level ?? "no data"}</p>
    <p>Score: ${player.score ?? "no data"}</p>
  `;
  return playerDiv;
}
