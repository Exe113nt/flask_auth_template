

// function updateTextInput(val) {
//     document.getElementById('textInput').textContent=val; 
//     console.log(val)
//   }


const rangeInputElement = document.querySelector('.form-control-range');
console.log('script')

rangeInputElement.addEventListener('change', (event) => {
    document.getElementsByClassName('textInput')[0].textContent=rangeInputElement.value; 
    console.log(rangeInputElement.value)
});