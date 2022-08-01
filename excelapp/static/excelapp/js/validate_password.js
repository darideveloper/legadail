const form = document.querySelector ("form")
const input_pass1 = document.querySelector ("#password1")
const input_pass2 = document.querySelector ("#password2")
const submit_button = document.querySelector ('input[type="submit"]')
const error_pass1 = document.querySelector ('.pass1-error')
const error_pass2 = document.querySelector ('.pass2-error')

input_pass1.addEventListener ("change", function (e) {
    // validate content of password 1: lower, upper, number and length
    let password_valid = false
    const password = input_pass1.value
    const hasNumber = /\d/
    if (password != password.toLowerCase() 
        && password != password.toUpperCase()
        && hasNumber.test (password)
        && password.length >= 8) {
        password_valid = true
    }

    if (password_valid) {
        // Clean error in first password
        error_pass1.innerHTML = ""
        input_pass1.removeAttribute ("invalid")
    } else {
        // Show error in first password
        input_pass1.setAttribute ("invalid", true)
        error_pass1.innerHTML = "<p> The password should have uppercase, lowercase, numbers and 8 characters</p>"
    }
})

input_pass2.addEventListener ("change", function (e) {
    // Validate if passwords match
    if (input_pass1.value == input_pass2.value) {
        // Remove error in second password
        input_pass2.removeAttribute ("invalid")
        error_pass2.innerHTML = ""

        // Enable submit button
        submit_button.removeAttribute ("disabled", false)
    } else {
        // Show error in second password
        input_pass2.setAttribute ("invalid", true)
        error_pass2.innerHTML = "<p> The passwords don't match</p>"
    }
})