function uploadVideo(e) {
  const input = document.getElementById("file_upload");

  const formData = new FormData();

  const file = input.files[0];
  console.log("i am here", file);
  formData.append("file", file);
  formData.append("name", file.name);
  fetch("https://forestfiredetection.azurewebsites.net//ForestFire/", {
    method: "POST",
    body: formData,
  })
    .then((res) => {
      return res.json();
    })
    .then((res) => {
      if (res.Msg == "Fire") {
       console.log(res.Msg);
       alert('Raging Fire Alert! \n Fire has been detected in your area! \n Send in the fire control crew immedietly')
     }
     else if (res.Msg == "Start Fire") {
      alert('Fire Alert! \n Smoke detected in your area. Possibility of fire! \n Send in the fire control crew before any damage is done.')
    }else{
      alert('No Fire Detected! \n The area is safe!')
    }
    });
}
