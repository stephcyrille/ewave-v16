var observeDOM = (function(){
  var MutationObserver = window.MutationObserver || window.WebKitMutationObserver;

  return function( obj, callback ){
    if( !obj || obj.nodeType !== 1 ) return;

    if( MutationObserver ){
      // define a new observer
      var mutationObserver = new MutationObserver(callback)

      // have the observer observe foo for changes in children
      mutationObserver.observe( obj, { childList:true, subtree:true })
      return mutationObserver
    }

    // browser support fallback
    else if( window.addEventListener ){
      obj.addEventListener('DOMNodeInserted', callback, false)
      obj.addEventListener('DOMNodeRemoved', callback, false)
    }
  }
})()

var addProductBtn = document.getElementById("addProductTrigger");
var listTabElm = document.getElementById("navitemTab");

// Product increment
var i = 1

function addProductTab (e){
  var itemHTML = `
  <div id=productTab${i+1} class="container tab-pane fade pl-3 pr-3"><br />
    <div class="form-group row">
      <label for=item_description${i+1} class="col-sm-3 col-form-label" >Item description <sup>*</sup></label>
      <div class="col-sm-9">
        <textarea class="form-control" type="text" id=item_description${i+1} name=item_description${i+1} placeholder="More about our item description " required="1"></textarea>
      </div>
    </div>
    <div class="form-group row">
      <label for=quantity${i+1} class="col-sm-3 col-form-label" >Quantity needed <sup>*</sup></label>
      <div class="col-sm-9">
        <input class="form-control" value="1" type="number" id=quantity${i+1} name=quantity${i+1} min="1" placeholder="Quantity needed" required="1"/>
      </div>
    </div>
    <div class="form-group row">
      <label for=item_weight${i+1} class="col-sm-3 col-form-label" >Weight (Kg) <sup>*</sup></label>
      <div class="col-sm-9">
        <input class="form-control" type="number" step="0.01" id=item_weight${i+1} name=item_weight${i+1} value="1.0" min="0" placeholder="Weight in Kg" required="1"/>
      </div>
    </div>
    <div class="form-group row">
      <label for=item_capacity${i+1} class="col-sm-3 col-form-label" >Capacity (m3) <sup>*</sup></label>
      <div class="col-sm-9">
        <input class="form-control" type="number" step="0.01" id=item_capacity${i+1} name=item_capacity${i+1} value="1.0" min="0" placeholder="Capacity in m3" required="1"/>
      </div>
    </div>
  </div>`

  var listBodyElm = document.getElementById("myTabContent");
  listBodyElm.insertAdjacentHTML("beforeend", itemHTML);
}

function addNavItem (e){
  var itemHTML = `
  <li class="nav-item custom-nav_item">
    <a class="nav-link" data-toggle="tab" href=#productTab${i+1}>
      Item ${i+1} <i class="fa fa-times-circle close_product_tab text-danger" id=closeProduct${i+1}></i>
    </a>
  </li>`

  var listTabElm = document.getElementById("navitemTab");
  console.log('Tab list obj----', listTabElm)
  listTabElm.insertAdjacentHTML("beforeend", itemHTML);
}

addProductBtn.onclick = function(e){
  if(i <= 30){
    addNavItem()
    addProductTab()
    i++
    console.log("Value of ", i)
    document.getElementsByName("product_counter")[0].value = i
  } else {
    alert("You cannot add more than 30 products !")
  }
}

// delete item
listTabElm.onclick = function(e){
  console.log("On clicked", e.target.parentNode.getAttribute("href"));
  if( e.target.nodeName == "I" ){
    // get the id of element for tab pane deletion
    var a_ref = e.target.parentNode.getAttribute("href");
    var pane_id = a_ref.replace(/^#+/i, '');

    console.log("Identifiant pane ", pane_id)
    // Remove pane value
    document.getElementById(pane_id).remove();
    // Remove tab pane
    e.target.parentNode.parentNode.removeChild(e.target.parentNode);

    // Set item 1 active by default
    var homeTab = document.getElementById("home");
    var navHomeTab = document.getElementById("nav1");
    homeTab.className = "container tab-pane active"
    navHomeTab.className = "nav-link active"
    i--
  }
}

// Observe a specific DOM element:
observeDOM( listTabElm, function(m){
   var addedNodes = [], removedNodes = [];

   m.forEach(record => record.addedNodes.length & addedNodes.push(...record.addedNodes))

   m.forEach(record => record.removedNodes.length & removedNodes.push(...record.removedNodes))

  //console.clear();
  console.log('Added:', addedNodes, 'Removed:', removedNodes);
});
