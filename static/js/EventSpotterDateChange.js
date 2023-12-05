$(document).ready(function(){
    $('.card-text').each(function (index){
        const date = new Date($(this).text() + "T00:00:00Z");
        if(date instanceof Date && !isNaN(date.valueOf())){
            date.setDate(date.getDate() + 1);
            const finalDate = date.toDateString();
            $(this).text(finalDate);
        }
    })
})