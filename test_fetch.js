const API_BASE = "https://cj.lziapi.com/api.php/provide/vod/?ac=detail&t=46&pg=1";
fetch(API_BASE)
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error("Error:", error));
