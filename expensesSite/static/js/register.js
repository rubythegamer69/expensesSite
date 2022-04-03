const usernameField=document.querySelector('#usernamefield');
const emailField= document.querySelector('#emailfield');
const userDisplay=document.querySelector('.invalid-feedback');
const emailDisplay=document.querySelector('.invalid-email');
const passwordToggle = document.querySelector('.togglePass');
const passwordField = document.querySelector('#passwordfield');
const submitButton = document.querySelector('.submit-btn');

const showHidePass = (e) =>{
    if (passwordToggle.textContent==="SHOW"){
        passwordToggle.textContent="HIDE"
        passwordField.setAttribute ("type","text")
    }else { 
        passwordToggle.textContent="SHOW"
        passwordField.setAttribute ("type","password")
    }

}

passwordToggle.addEventListener('click',showHidePass);





emailField.addEventListener("keyup",(e)=>{
    
    const emailVal = e.target.value;

    emailField.classList.remove("is-invalid");
    emailDisplay.style.display="none";
    submitButton.removeAttribute ("disabled");
   
    if (emailVal.length > 0) {
        fetch("/authentication/validate-email",{
            body: JSON.stringify({email: emailVal}),
            method: "POST",
        }) 
        .then((res)=> res.json())
        .then((data)=> {
            console.log("data",data)
            if (data.email_error) {
                submitButton.disabled = true;
                emailField.classList.add("is-invalid");
                emailDisplay.style.display="block";
                emailDisplay.innerHTML=`<p>${data.email_error}</p>`;
            }
        })

    }
    
})


usernameField.addEventListener("keyup",(e)=>{
    
    const uNameVal = e.target.value;

    usernameField.classList.remove("is-invalid");
    userDisplay.style.display="none";
    submitButton.removeAttribute ("disabled");
   
    if (uNameVal.length > 0) {
        fetch("/authentication/validate-username",{
            body: JSON.stringify({username: uNameVal}),
            method: "POST",
        }) 
        .then((res)=> res.json())
        .then((data)=> {
            console.log("data",data)
            if (data.username_error) {
                submitButton.disabled= true;
                usernameField.classList.add("is-invalid");
                userDisplay.style.display="block";
                userDisplay.innerHTML=`<p>${data.username_error}</p>`;
            }
        })

    }
    
})