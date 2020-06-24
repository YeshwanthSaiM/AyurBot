var data=[];

function addBr(text){
    return text.replace(/\n/g, "<br />");
}
var Message;
Message = function (arg) {
    this.text = arg.text, this.message_side = arg.message_side;
    this.draw = function (_this) {
        return function () {
            var $message;
            $message = $($('.message_template').clone().html());
            $message.addClass(_this.message_side).find('.text').html(addBr(_this.text));
            $('.messages').append($message);
            return setTimeout(function () {
                return $message.addClass('appeared');
            }, 0);
        };
    }(this);
    return this;
};

function showBotMessage(msg){
        message = new Message({
             text: msg,
             message_side: 'left'
        });
        message.draw();
        $messages.animate({ scrollTop: $messages.prop('scrollHeight') }, 300);
}
function showUserMessage(msg){
        $messages = $('.messages');
        message = new Message({
            text: msg,
            message_side: 'right'
        });
        message.draw();
        $messages.animate({ scrollTop: $messages.prop('scrollHeight') }, 300);
        $('#msg_input').val('');
}
function sayToBot(text, button){
    document.getElementById("msg_input").placeholder = "Type your messages here..."
    if(button == "text"){
        $.post("/chat",
        {
            //csrfmiddlewaretoken:csrf,
            text:text,
        },
        function(jsondata, status){
            if(jsondata["status"]=="success"){
                response=jsondata["response"];

                if(response){showBotMessage(response);}
            }
        });
    }else{

        $.post("/chat",
        {
            //csrfmiddlewaretoken:csrf,
            text:text,
        },
        function(jsondata, status){
            if(jsondata["status"]=="success"){
                response=jsondata["response"];

                if(response){showBotMessage(response);}
            }
        });
    }
}

function addToInput(text){
    var text = "Sample text"
    document.getElementById("msg_input").placeholder = text;
}

getMessageText = function () {
            var $message_input;
            $message_input = $('.message_input');
            return $message_input.val();
        };

$("#say").keypress(function(e) {
    if(e.which == 13) {
        $("#saybtn").click();
    }
});

$('.send_message').click(function (e) {
        msg = getMessageText();
        if(msg){
        showUserMessage(msg, "test");
        sayToBot(msg);
    $('.message_input').val('');}
});

$('.speech-icon').click(function (e) {
    // This function makes: when speech-icon is clicked 
    // the voice is recorded and converted to the text 
    // stored in the input box
    $.post("/speak",
        {
            text:"dummy",
        },
        function(jsondata, status){
            if(jsondata["status"]=="success"){
                response=jsondata["response"];
                if(response){
                    $('.message_input').val(response)
                }
            }
        });
});


$('.send_voice').click(function (e) {
    msg = getMessageText();
    if(msg){
    showUserMessage(msg, "voice");
    sayToBot(msg);
$('.message_input').val('');}
});


$('.message_input').keyup(function (e) {
    if (e.which === 13) {
        msg = getMessageText();
        if(msg){
        showUserMessage(msg);
        sayToBot(msg);
    $('.message_input').val('') ;}
    }
});
