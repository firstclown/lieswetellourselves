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
    YAHOO.util.Event.addListener('vote_up', 'click', vote_up, this);
    YAHOO.util.Event.addListener('vote_down', 'click', vote_down, this);
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

function vote_up(e, element){
    var callback =
	{
	  success: function(o) {/*success handler code*/},
	  failure: function(o) {/*failure handler code*/},
	  timeout: 5000,
	}
    var id = element.id.match(/\d+/)[0];
    var transaction = YAHOO.util.Connect.asyncRequest('POST', '/lies/add_vote/', callback, "vote=up&lie_id="+id);
    YAHOO.util.Event.preventDefault(e);
}
function vote_down(e, element){
    var callback =
	{
	  success: function(o) { },
	  failure: function(o) { },
	  timeout: 5000,
	}
    var id = element.id.match(/\d+/)[0];
    var transaction = YAHOO.util.Connect.asyncRequest('POST', '/lies/add_vote/', callback, "vote=down&lie_id="+id);
    YAHOO.util.Event.preventDefault(e);

}

function init(){
    var allLies = YAHOO.util.Dom.getElementsByClassName('lie_item');
    YAHOO.util.Event.addListener(allLies, 'mouseover', show_vote);
    YAHOO.util.Event.addListener(allLies, 'mouseout', hide_vote);
}

YAHOO.util.Event.onDOMReady(init);
