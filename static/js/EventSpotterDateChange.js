$(document).ready(function(){
    $('.card-text').each(function (index){
        const date = new Date($(this).text());
        if(date instanceof Date && !isNaN(date.valueOf())){
            const finalDate = date.toDateString();
            $(this).text(finalDate);
        }
    })
})