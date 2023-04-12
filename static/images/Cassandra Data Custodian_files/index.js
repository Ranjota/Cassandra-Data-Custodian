$(document).ready(function() {
    loadDropDowns();
});

function loadDropDowns() {
    academicPeriod = ['Summer', 'Winter', 'Fall'];
    year = ['2019', '2020', '2021'];
    ethnicity = ['Pacific Islander', 'Black', 'Hispanic', 'South Asian', 'Alaska Native', 'Asian']
    georgian_campus = ['Barrie', 'Collingwood', 'Owen Sound', 'Midland', 'Orangeville', 'Orillia', 'Muskoka', 'ILAC']
    gender = ['Male', 'Female']
    groups = ['Group A', 'Group B', 'Group C', 'Group D']
    programCode = ['BAGM', 'MDEV', 'OFAE', 'AIDI', 'GBMT', 'OFAG', 'BDAT', 'HRMN', 'CULN']

    for(var i=0; i<academicPeriod.length; i++) {
        for(var j=0; j < year.length; j++) {
            $('#inputAcademicPeriod').append('<option value="' + academicPeriod[i] + year[j] + '" >' + academicPeriod[i] + " " + year[j] + '</option>')
        }
    }

    for(var i=0; i<ethnicity.length; i++) {
        $('#inputEthnicity').append('<option value="' + ethnicity[i]  + '" >' + ethnicity[i] + '</option>')
    }

    for(var i=0; i< georgian_campus.length; i++) {
        $('#inputGCCampus').append('<option value="' + georgian_campus[i]  + '" >' + georgian_campus[i] + '</option>')
    }

    year = 1990;
    while(year <= 2023) {
        $('#inputBirthYear').append('<option value="' + year + '" >' + year + '</option>')
        year++;
    }

    for(var i=0; i< gender.length; i++) {
        $('#inputGender').append('<option value="' + gender[i]  + '" >' + gender[i] + '</option>')
    }

    for(var i=0; i< groups.length; i++) {
        $('#inputGroups').append('<option value="' + groups[i]  + '" >' + groups[i] + '</option>')
    }

    for(var i=0; i< programCode.length; i++) {
        $('#inputProgramCode').append('<option value="' + programCode[i]  + '" >' + programCode[i] + '</option>')
    }

    $('select').css("color", "gray");
}



function onOptionSelected(event) {
    // alert($('select option:selected').val())
    $(event).css('color', 'black');
}
