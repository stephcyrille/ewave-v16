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
var tab_counter = 1

function addProductTab (e){
  var itemHTML = `
  <div class="tab-pane fade" id=nav_product_${i+1} role="tabpanel"
       aria-labelledby=nav_product_${i+1}_tab><br />
    <div class="form-group row my-3">
      <label for=product_name_${i+1} class="col-sm-3 col-form-label" >Name <sup>*</sup></label>
      <div class="col-sm-9">
        <input class="form-control" type="text" id=product_name_${i+1} name=product_name_${i+1} placeholder="Product name" required="1"/>
      </div>
    </div>
    <div class="form-group row my-3">
      <label for=product_material_${i+1} class="col-sm-3 col-form-label">Material <sup>*</sup></label>
      <div class="col-sm-9">
        <select class="form-control" id=product_material_${i+1} name=product_material_${i+1}
                  placeholder="Product material">
            <option value="other">Other</option>
            <option value="electronic">Electronic</option>
            <option value="textile">Textile</option>
            <option value="cosmetic">Cosmetic</option>
            <option value="shoes">Shoes</option>
        </select>
      </div>
    </div>
    <div class="form-group row my-3">
      <label for=quantity_${i+1} class="col-sm-3 col-form-label" >Quantity <sup>*</sup></label>
      <div class="col-sm-9">
        <input class="form-control" value="1" type="number" id=quantity_${i+1} name=quantity_${i+1} min="1" placeholder="Quantity needed" required="1"/>
      </div>
    </div>
    <div class="form-group row my-3">
      <label for=product_weight_${i+1} class="col-sm-3 col-form-label" >Weight <sup>*</sup></label>
      <div class="col-sm-9">
      <input class="form-control" value="1.0" type="number" step="0.01"
                                   id=product_weight_${i+1} name=product_weight_${i+1} min="1"
                                   placeholder="Weight in Kg" required="1" />
      </div>
    </div>
    <div class="form-group row my-3">
      <label for=product_capacity_${i+1} class="col-sm-3 col-form-label" >Capacity <sup>*</sup></label>
      <div class="col-sm-9">
      <input class="form-control" value="1.0" type="number" step="0.01"
                                   id=product_capacity_${i+1} name=product_capacity_${i+1} min="1"
                                   placeholder="Weight in Kg" required="1" />
      </div>
    </div>
    <div class="form-group row my-3">
      <label for=product_price_${i+1} class="col-sm-3 col-form-label" >Price <sup>*</sup></label>
      <div class="col-sm-9">
      <input class="form-control" value="1.0" type="number" step="0.01"
                                   id=product_price_${i+1} name=product_price_${i+1} min="1"
                                   placeholder="Estimated price (XAF)" required="1" />
      </div>
    </div>
  </div>`

  var listBodyElm = document.getElementById("myTabContent");
  listBodyElm.insertAdjacentHTML("beforeend", itemHTML);
}

function addNavItem (e){
  var itemHTML = `
  <button class="nav-link" id=nav_product_${i+1}_tab data-bs-toggle="tab"
          data-bs-target=#nav_product_${i+1} type="button" role="tab"
          aria-controls=nav_product_${i+1} aria-selected="false">
    Product ${i+1} <i class="fa fa-times-circle close_product_tab text-danger" id=closeProduct${i+1}></i>
  </button>`

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
    tab_counter++
    console.log("Value of ", i)
    document.getElementsByName("product_counter")[0].value = tab_counter
    new_tab_key = `nav_product_${i}_tab`
    document.getElementById(new_tab_key).click()
  } else {
    alert("You cannot add more than 30 products !")
  }
}

// delete item
listTabElm.onclick = function(e){
  if( e.target.nodeName == "I" ){
    var tab_id = e.target.parentNode.getAttribute("id");
    var tap_pane = e.target.parentNode.getAttribute("aria-controls");

    document.getElementById(tab_id).remove();
    document.getElementById(tap_pane).remove();

    new_tab_key = `nav_product_${i-1}_tab`
    if(document.getElementById(new_tab_key)){
        document.getElementById(new_tab_key).click()
    } else {
        document.getElementById('nav_product_1_tab').click()
    }
    tab_counter--
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



