function show_vote(e) {
    var location = YAHOO.util.Dom.getXY(this);
    var itemRegion = YAHOO.util.Region.getRegion(this);
    var itemHeight = itemRegion.bottom - itemRegion.top;
    var itemWidth = itemRegion.right - itemRegion.left;
    var voteRegion = YAHOO.util.Region.getRegion(document.getElementById('vote'));
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

function ajax_vote(e, element){
    var callback =
	{
	  success: function(o) { 
          var vote_display = YAHOO.util.Dom.getFirstChildBy(element, function(e){return e.className == 'vote_total';})
          var vote = YAHOO.lang.JSON.parse(o.responseText);
          vote_display.innerHTML = vote.vote_total_value;
      },
	  failure: function(o) {
          var message_area = document.getElementById('message');
          message_area.innerHTML = "Can't currently connect to server. Imagine a Fail Whale picture here.";
          var anim_message = new YAHOO.util.Anim('message', { opacity: { from: 0,to: 1 }}, 1, YAHOO.util.Easing.easeIn);
          anim_message.animate();
      },
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

function init(){
    var allLies = YAHOO.util.Dom.getElementsByClassName('lie_item');
    YAHOO.util.Event.addListener(allLies, 'mouseover', show_vote);
    YAHOO.util.Event.addListener(allLies, 'mouseout', hide_vote);
}

YAHOO.util.Event.onDOMReady(init);
