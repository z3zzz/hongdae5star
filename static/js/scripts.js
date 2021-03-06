function buttonForRegisterClicked(){
    console.log("Hello!");
    let data = {
        "user_id": $("#inputIdRegister").val(),
        "user_pw": $("#inputPwRegister").val(),
        "user_nickname": $("#inputNicknameRegister").val(),
        "favorite_food": $("#inputFavoriteFoodRegister").val()
    };

    var errorPlace = document.querySelector("#errorMessage");

    if(data['user_id'].length < 5){
        errorPlace.textContent = "Id should be longer than 4";
        errorPlace.classList.remove('error-hidden');
        return;
    };
    if(data['user_pw'].length < 5){
        errorPlace.textContent = "Password should be longer than 4";
        errorPlace.classList.remove('error-hidden');
        return;
    };

    if(data['user_nickname'].length < 2){
        errorPlace.textContent = "Nickname should be longer than 1";
        errorPlace.classList.remove('error-hidden');
        return;
    };

    if(data['favorite_food'].length < 1){
        errorPlace.textContent = "Please advise your favorite food!";
        errorPlace.classList.remove('error-hidden');
        return;
    };

    $.ajax({
        url: "/register",
        type: "post",
        data: data,
        datatype: "json",
        success: function(resp) {
            console.log(resp);
            alert("Register success!\nPlease login.");
            window.location.href = '/login'
        },
        error: function(resp) {
            console.log(resp);
            errorPlace.textContent = resp.responseJSON.error;
            errorPlace.classList.remove('error-hidden');
        }
    });

};

function buttonForLoginClicked(){
    console.log("Hello!");
    let data = {
        "user_id": $("#inputIdLogin").val(),
        "user_pw": $("#inputPwLogin").val(),
    };

    var errorPlace = document.querySelector("#errorMessage");

    if(data['user_id'].length == 0 || data['user_pw'] == 0){
        errorPlace.textContent = "Please enter your id and password";
        errorPlace.classList.remove('error-hidden');
        return;
    }
    if(data['user_id'].length < 5){
        errorPlace.textContent = "Please enter correct id, or register";
        errorPlace.classList.remove('error-hidden');
        return;
    };
    if(data['user_pw'].length < 5){
        errorPlace.textContent = "Please enter correct password, or register ";
        errorPlace.classList.remove('error-hidden');
        return;
    };

    $.ajax({
        url: "/login",
        type: "post",
        data: data,
        datatype: "json",
        success: function(resp) {
            console.log(resp);
            alert("Login success!");
            window.location.href = '/mypage'
        },
        error: function(resp) {
            console.log(resp);
            errorPlace.textContent = resp.responseJSON.error;
            errorPlace.classList.remove('error-hidden');
        }
    });

};

function email_for_alert(){
    let email_address = $('#emailForAlert').val()
    if(validate_email(email_address) == false){
        alert("Not a valid email format..")
        return;
    }

    $.ajax({
        url: "/email-for-alert",
        type: "post",
        data: {"email_address":email_address},
        success: function(res){
            console.log(res)
            if(res["result"] == "success"){
            var success_text = email_address + " is successfully submitted!";
            alert(success_text);
            return;
            } else{
                var fail_text = email_address + " is already in our alert-email list!";
                alert(fail_text);
                return;
            }
        }
    })
}

function validate_email(email){
    var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    return regex.test(email);
}

function linkMyFoodList(){
    console.log("let's go to my food list!")
    window.location.href='/mypage/foodlist'
}

function linkMyNote(){
    window.location.href = "/mypage/note"
}


addNewFood = () => {
    let store_name = $("input[name='inputStoreName']").val()
    let menu = $("input[name='inputMenu']").val()
    let location = $("input[name='inputLocation']").val()
    let additional_info = $("textarea[name='inputExtraInfo']").val()
    let author = '{{ session["current_user"] }}'

    error_text = document.getElementById('addNewFoodError')
    if(store_name == ""){
        error_text.textContent = "Please input store name.."
        return;
    }
    if(menu == ""){
        error_text.textContent = "Please input menu.."
        return;
    }

    $.ajax({
        url: '/mypage/foodlist',
        type: 'post',
        data: {
            "store_name": store_name,
            "menu": menu,
            "location": location,
            "additional_info": additional_info,
            "author": author
        },
        success: (res) => {
            console.log(res);
            alert(res["result"]);
            window.location.reload()
        },
        error: (res) => {
            alert(res["result"]);
        }
    })

}

deleteFood = (e) => {
    var food_id = e.currentTarget.id
    $.ajax({
        url: "/mypage/foodlist",
        type: "delete",
        data: {
            "food_id": food_id
        },
        success: (res) => {
            alert(res['result'])
            window.location.reload()
        },
        error: (res) => {
            console.log(res["result"])
            alert("Failed to delete..sorry")
        }
    })
}

addDeleteFoodListFunction = elem => {
    elem.addEventListener("click",deleteFood)
}

notReadyYet = () => {
    alert("This page or function is not ready yet.. will update soon!");
    return;
}

addNotReadyFunction = elem => {
    elem.addEventListener("click",notReadyYet)
}

togglePrivatePublicStatus = e => {
    let elem = e.target
    let current_status = elem.dataset.food_status
    let food_id = elem.id

    let data = {
        "isPrivate": current_status,
        "food_id": food_id
    }

    $.ajax({
        url: "/mypage/foodlist",
        type: "patch",
        contentType: "application/json",
        data: JSON.stringify(data),
        success: (res) => {
            console.log(res["result"])
        },
        error: (res) => {
            console.log(res["result"])
        }
    })

    if(current_status=="True"){
        elem.innerText="Public"
        elem.classList.remove("btn-info")
        elem.classList.add("btn-success")
        elem.dataset.food_status="False"
    }else{
        elem.innerText="Private"
        elem.classList.remove("btn-success")
        elem.classList.add("btn-info")
        elem.dataset.food_status="True"
    }
}

addToggleProperty = elem => {
    if(elem.dataset.food_status=="True"){
        elem.innerText="Private"
        elem.classList.add("btn-info")
    }else{
        elem.innerText="Public"
        elem.classList.add("btn-success")
    }
    elem.addEventListener("click", togglePrivatePublicStatus)
}

addBackgroundForFoodList = elem => {
    if(elem.dataset.foodlist_author == elem.dataset.current_user){
        elem.classList.add("bg-whitegreen")
    }else{
        elem.classList.add("bg-whiteBlue")
    }
}

saveNote = async e => {
    let user_id = e.target.dataset.user_id
    let note1 = document.querySelector('#note1').value
    let note2 = document.querySelector('#note2').value
    let note3 = document.querySelector('#note3').value
    let note4 = document.querySelector('#note4').value

    let data = {
            _id: user_id,
            note1: note1,
            note2: note2,
            note3: note3,
            note4: note4
        }

    res = await fetch('/mypage/note', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    temp = await res.json()
    console.log(temp)
    let messageSpace = document.querySelector('#spaceForSaveCompletedMessage')
    messageSpace.classList.remove('fade-out')
    messageSpace.style.opacity = null
    messageSpace.innerText = temp.result
    messageSpace.style.color = 'blue'
    setTimeout(() => {
        messageSpace.classList.add('fade-out')
    }, 100)
}


let notReadyElements = document.querySelectorAll('.notReadyYet')
notReadyElements.forEach(addNotReadyFunction)

let deleteFoodButtons = document.querySelectorAll('.deleteFoodList')
deleteFoodButtons.forEach(addDeleteFoodListFunction)

let addNewFoodButton = document.querySelector('#newFoodAdd')
if(addNewFoodButton) addNewFoodButton.addEventListener("click", addNewFood)

let toggle_buttons = document.querySelectorAll('.togglePrivatePublic')
toggle_buttons.forEach(addToggleProperty)

let divsForBackground = document.querySelectorAll(".cardBackgroundColor")
divsForBackground.forEach(addBackgroundForFoodList)

let noteButton = document.querySelector('#buttonForNoteSave')
if (noteButton) noteButton.addEventListener("click", saveNote)


console.log(window.location)
