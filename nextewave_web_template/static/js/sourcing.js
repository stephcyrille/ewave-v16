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
  <div id=productTab${i+1} class="container tab-pane fade"><br />
    <div class="form-group row">
      <label for=product_name${i+1} class="col-sm-3 col-form-label" >Product name</label>
      <div class="col-sm-9">
        <input class="form-control" type="text" id=product_name${i+1} name=product_name${i+1} placeholder="Product name" required="0"/>
      </div>
    </div>
    <div class="form-group row">
      <label for=product_picture${i+1} class="col-sm-3 col-form-label">Product picture</label>
      <div class="col-sm-9">
        <input type="file" class="form-control-file" name=product_picture${i+1} accept="image/jpeg,image/gif,image/png" />
      </div>
    </div>
    <div class="form-group row">
      <label for=quantity${i+1} class="col-sm-3 col-form-label" >Quantity needed <sup>*</sup></label>
      <div class="col-sm-9">
        <input class="form-control" value="1" type="number" id=quantity${i+1} name=quantity${i+1} min="1" placeholder="Quantity needed" required="1"/>
      </div>
    </div>
    <div class="form-group row">
      <label for=product_description${i+1} class="col-sm-3 col-form-label" >Product description <sup>*</sup></label>
      <div class="col-sm-9">
        <textarea class="form-control" type="text" id=product_description${i+1} name=product_description${i+1} placeholder="More about our product description " required="1"></textarea>
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
      Product ${i+1} <i class="fa fa-times-circle close_product_tab text-danger" id=closeProduct${i+1}></i>
    </a>
  </li>`

  var listTabElm = document.getElementById("navitemTab");
  console.log('Tab list obj----', listTabElm)
  listTabElm.insertAdjacentHTML("beforeend", itemHTML);
}

addProductBtn.onclick = function(e){
  e.preventDefault();

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

    // Remove pane value
    document.getElementById(pane_id).remove();
    // Remove tab pane
    e.target.parentNode.parentNode.removeChild(e.target.parentNode);

    i--
  } else {
    if(e.target.getAttribute("href")){
        console.log("bimmmmmm=============", e.target.getAttribute("href"));
        window.location.hash = e.target.getAttribute("href");
    }
  }
}

// Observe a specific DOM element:
observeDOM( listTabElm, function(m){
   var addedNodes = [], removedNodes = [];

   m.forEach(record => record.addedNodes.length & addedNodes.push(...record.addedNodes))

   m.forEach(record => record.removedNodes.length & removedNodes.push(...record.removedNodes))

  console.clear();
  console.log('Added:', addedNodes, 'Removed:', removedNodes);
});

