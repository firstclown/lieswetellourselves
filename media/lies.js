var LIES;

function show_vote(e) {
    var location = YAHOO.util.Dom.getXY(this);
    var itemRegion = YAHOO.util.Region.getRegion(this);
    var itemHeight = itemRegion.bottom - itemRegion.top;
    var itemWidth = itemRegion.right - itemRegion.left;
    var voteRegion = YAHOO.util.Region.getRegion(YAHOO.util.Dom.get('vote'));
    var voteHeight = voteRegion.bottom - voteRegion.top;
    var voteWidth = voteRegion.right - voteRegion.left;
    YAHOO.util.Dom.setX('vote', location[0] + itemWidth/2 - voteWidth/2);
    YAHOO.util.Dom.setY('vote', location[1] + itemHeight/2 - voteHeight/2);
    
    YAHOO.util.Event.removeListener('vote_up', 'click');
    YAHOO.util.Event.removeListener('vote_down', 'click');
    YAHOO.util.Event.addListener('vote_up', 'click', ajax_vote, this);
    YAHOO.util.Event.addListener('vote_down', 'click', ajax_vote, this);
    YAHOO.util.Dom.setStyle('vote', 'visibility', 'visible');
}

function hide_vote(e){
    var mousePos = new YAHOO.util.Point(YAHOO.util.Event.getXY(e));
    if(!YAHOO.util.Region.getRegion(this).contains(mousePos)){
        YAHOO.util.Dom.setStyle('vote', 'visibility', 'hidden');
        YAHOO.util.Event.removeListener('vote_up', 'click');
        YAHOO.util.Event.removeListener('vote_down', 'click');
    }
}

function display_failure(o){
    var message_area = YAHOO.util.Dom.get('message');
    message_area.innerHTML = "Can't currently connect to server. Imagine a Fail Whale picture here.";
    var anim_message = new YAHOO.util.Anim('message', { opacity: { from: 0,to: 1 }}, 1, YAHOO.util.Easing.easeIn);
    anim_message.animate();
    window.clearInterval(LIES.interval);
}
function ajax_vote(e, element){
    var callback =
	{
	  success: function(o) { 
          var vote_display = YAHOO.util.Dom.getFirstChildBy(element, function(e){return e.className == 'vote_total';})
          if(o.responseText != 'dupe'){
              var vote = YAHOO.lang.JSON.parse(o.responseText);
              vote_display.innerHTML = vote.vote_total_value;
              var flash_vote = new YAHOO.util.ColorAnim(vote_display, { 'color': { from: '#FFFF00', to: '#060080' }}, 2, YAHOO.util.Easing.easeIn);
              flash_vote.animate();
             // update_list();
          }
      },
	  failure: display_failure,
	  timeout: 5000,
	}
    var id = element.id.match(/\d+/)[0];
    var target = YAHOO.util.Event.getTarget(e);
    //Must get parent because, even though listener is on A tag,
    //it will pass the img element here
    var type = target.parentNode.id.match(/vote_(.+)/)[1];
    var transaction = YAHOO.util.Connect.asyncRequest('POST', '/lies/add_vote/', callback, "vote="+type+"&lie_id="+id);
    YAHOO.util.Event.preventDefault(e);
}

function ajax_add(e){
    var callback =
	{
	  success: function(o) { 
          YAHOO.util.Dom.get('id_lie').value = '';
          update_list();
      },
	  failure: display_failure,
	  timeout: 5000,
	}
    var lie = YAHOO.util.Dom.get('id_lie').value;
    //Must get parent because, even though listener is on A tag,
    //it will pass the img element here
    var transaction = YAHOO.util.Connect.asyncRequest('POST', '/lies/add/', callback, "lie="+lie);
    YAHOO.util.Event.preventDefault(e);
}

function update_list(){
    var callback = {
        success: function(o){
            var lies = YAHOO.lang.JSON.parse(o.responseText);
            var list = YAHOO.util.Dom.get('lie_list');
            var old_elements = YAHOO.util.Dom.getChildren(list);
            for(var i in old_elements){
                list.removeChild(old_elements[i]);
            }
            for(var i in lies){
                var new_element = document.createElement('li');
                new_element.id = "lie_"+lies[i].id;
                YAHOO.util.Dom.addClass(new_element, 'lie_item');
                var vote_span = document.createElement('span');
                YAHOO.util.Dom.addClass(vote_span, 'vote_total');
                vote_span.innerHTML = lies[i].vote_total_value;
                new_element.appendChild(vote_span);
                var lie_span = document.createElement('span');
                YAHOO.util.Dom.addClass(lie_span, 'lie');
                lie_span.innerHTML = lies[i].lie;
                new_element.appendChild(lie_span);
                list.appendChild(new_element);
            }
            registerListItems();
        },
        failure:display_failure,
        timeout:5000,
    }
    var transaction = YAHOO.util.Connect.asyncRequest('GET', '/lies/', callback);
}

function registerListItems(){
    var allLies = YAHOO.util.Dom.getElementsByClassName('lie_item');
    YAHOO.util.Event.addListener(allLies, 'mouseover', show_vote);
    YAHOO.util.Event.addListener(allLies, 'mouseout', hide_vote);
}

function init(){
    registerListItems();

    YAHOO.util.Event.addListener('add_lie_submit', 'click', ajax_add);
    YAHOO.util.Event.addListener('vote', 'mouseout', hide_vote);

    LIES.interval = window.setInterval(update_list, 10000);
}

YAHOO.util.Event.onDOMReady(init);
