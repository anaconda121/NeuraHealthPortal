// redirect user to output page after form submission 
function redirect() {
  window.location.replace("output.html");
  return false;
}

// take uploaded file and store it in location from which model can use it
const url = '../../templates/gui/upload.php'
const form = document.querySelector('form')

form.addEventListener('submit', (e) => {
    e.preventDefault();
    //console.log("hello!");

    const files = document.querySelector('[type=file]').files
    const formData = new FormData()

    for (let i = 0; i < files.length; i++) {
        let file = files[i]

        formData.append('files[]', file)
    }

    fetch(url, {
        method: 'POST',
        body: formData,
    }).then((response) => {
        console.log(response)
    })
});