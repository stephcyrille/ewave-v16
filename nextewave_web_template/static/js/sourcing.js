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
      <label for=product_name_${i+1} class="col-sm-3 col-form-label" >Product ${i+1}</label>
      <div class="col-sm-9">
        <input class="form-control" type="text" id=product_name_${i+1} name=product_name_${i+1} placeholder="Product name" required="0"/>
      </div>
    </div>
    <div class="form-group row my-3">
      <label for=product_picture_${i+1} class="col-sm-3 col-form-label">Picture</label>
      <div class="col-sm-9">
        <div class="row mb-3">
            <div class="col-sm-6 col-md-6">
              <div class="row">
                <input type="file" class="form-control-file" name=product_picture_${i+1}
                   accept="image/jpeg,image/gif,image/png" data-show-upload="true"
                   data-show-caption="true" lass="file" data-show-preview="true"
                   id=product_picture_${i+1} onchange="onAddPic(this)"
                />
              </div>
            </div>
            <div class="col-sm-6 col-md-6">
              <div class="row">
                <input type="file" class="form-control-file" name="product_picture_${i+1}_2"
                   accept="image/jpeg,image/gif,image/png" data-show-upload="true"
                   data-show-caption="true" lass="file" data-show-preview="true"
                   id="product_picture_${i+1}_2" onchange="onAddPic(this)"
                />
              </div>
            </div>
        </div>
        <div class="row">
            <div class="col-sm-6 col-md-6">
              <div class="row">
                <input type="file" class="form-control-file" name="product_picture_${i+1}_3"
                   accept="image/jpeg,image/gif,image/png" data-show-upload="true"
                   data-show-caption="true" lass="file" data-show-preview="true"
                   id="product_picture_${i+1}_3" onchange="onAddPic(this)"
                />
              </div>
            </div>
            <div class="col-sm-6 col-md-6">
              <div class="row">
                <input type="file" class="form-control-file" name="product_picture_${i+1}_4"
                   accept="image/jpeg,image/gif,image/png" data-show-upload="true"
                   data-show-caption="true" lass="file" data-show-preview="true"
                   id="product_picture_${i+1}_4" onchange="onAddPic(this)"
                />
              </div>
            </div>
        </div>
      </div>
    </div>
    <div class="form-group row my-3">
      <label for=quantity_${i+1} class="col-sm-3 col-form-label" >Quantity <sup>*</sup></label>
      <div class="col-sm-9">
        <input class="form-control" value="1" type="number" id=quantity_${i+1} name=quantity_${i+1} min="1" placeholder="Quantity needed" required="1"/>
      </div>
    </div>
    <div class="form-group row my-3">
      <label for=product_description_${i+1} class="col-sm-3 col-form-label" >Description <sup>*</sup></label>
      <div class="col-sm-9">
        <textarea class="form-control" type="text" id=product_description_${i+1} name=product_description_${i+1} placeholder="More about our product description " required="1"></textarea>
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

function onAddPic(input){
    var id_pic = input.id

    if (input.files && input.files[0]) {
        if (!document.getElementById(`${id_pic}_prev`)){
            var url = window.URL.createObjectURL(input.files[0])
            var prevElt = `<div class='row mt-1' id='${id_pic}_prev'>
                    <i class="fa fa-times text-danger text-center" onclick="delPrev(this)"/>
                    <img src=${url} style="width: 200px; height: 100px"/>
                </div>`
            document.getElementById(id_pic)
                .parentNode.insertAdjacentHTML("beforeend", prevElt);
        } else {
            document.getElementById(`${id_pic}_prev`).remove()
            var url = window.URL.createObjectURL(input.files[0])
            var prevElt = `<div class='row mt-1' id='${id_pic}_prev'>
                    <i class="fa fa-times text-danger text-center" onclick="delPrev(this)"/>
                    <img src=${url} style="width: 200px; height: 100px"/>
                </div>`
            document.getElementById(id_pic)
                .parentNode.insertAdjacentHTML("beforeend", prevElt);
        }
    }
}

function delPrev(elt){
    elt.parentNode.previousSibling.previousSibling.value= null;
    elt.parentNode.remove();
}

// Observe a specific DOM element:
observeDOM( listTabElm, function(m){
   var addedNodes = [], removedNodes = [];

   m.forEach(record => record.addedNodes.length & addedNodes.push(...record.addedNodes))

   m.forEach(record => record.removedNodes.length & removedNodes.push(...record.removedNodes))

  console.clear();
  console.log('Added:', addedNodes, 'Removed:', removedNodes);
});



