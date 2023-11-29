$("#btnRegisterParent").click(function (e) {
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

$('#registerLearner').click(function(e) {
    e.preventDefault();

    const name = $('#learnerName').val();
    const surname = $('#learnerSurname').val();
    const phone = $('#cellNumber').val();
    const grade = $('#grade').val();

    $.ajax({
        url: '/register/learner',
        type: 'POST',
        data: {
            f_name: name,
            l_name: surname,
            cell_no: phone,
            grade: grade
        },
        success: function (response) {
            console.log(response);
        },
        error: function(error) {
            console.log(error);
        }
    })

})