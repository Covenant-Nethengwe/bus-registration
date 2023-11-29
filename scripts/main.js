$("#btnRegisterParent").click(function (e) {
    alert('button have been clicked')
    e.preventDefault();
    
    const fName = $('#firstName').val();
    const lName = $('#lastName').val();
    const email = $('#email').val();
    const phone = $('#phone').val();
    const password = $('#password').val();

    $.ajax({
        url: '/register/parent',
        type: 'POST',
        data: {
            f_name: fName,
            l_name: lName,
            mail: email,
            cell_no: phone,
            pass: password
        },
        success: function (response) {
            console.log(response);
        },
        error: function(error) {
            console.log(error);
        }
    })

})

