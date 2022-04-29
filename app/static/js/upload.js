var fileupload = document.getElementById("upload")


fileupload.onchange = () => {
    uploadFile()
  }

async function uploadFile() {
    let formData = new FormData(); 
    formData.append("file", fileupload.files[0]);
    await fetch('/uploadfile', {
      method: "POST", 
      body: formData
    }); 
    location.reload()
    
    return false;
    }
