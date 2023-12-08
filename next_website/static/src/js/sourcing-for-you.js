// Dynamic Field Creation

const productList = document.querySelector("#products-list");
const productForm = productList.querySelector(".product-form");
const addProductButton = document.querySelector("#add-product");
//let size = productList.childElementCount;

addProductButton.addEventListener("click", addProduct);

/**
  * Increase the counter of products when we trigger on add button action
*/

 // Product increment
var size = 1;
var tab_counter = 1;


/**
 * removeProduct: the function remove a form for a new product
 */

function removeProduct(index) {
  var product_number = index.split('-')[1];

  if(product_number < tab_counter){
    console.log("You must select first the last product");
  } else {
    let element = document.getElementById(index);
    element.remove();
    tab_counter--;
    document.getElementsByName("product_counter")[0].value = tab_counter
    size--
  }

  console.log("Count items >>>>>>", tab_counter)
}

/**
 * addProduct: the function add a form for a new product
 */


function addProduct() {
  size++;
  tab_counter ++;

  document.getElementsByName("product_counter")[0].value = tab_counter;

  let element = productForm.cloneNode(true);
  let index = size;

  //Get element of the sub form product
  let title = element.querySelector("div > .product-title");
  let removeProductButton = element.querySelector("div > .remove-product");
  let name = element.querySelector(".product-infos > .product-name");
  let quantity = element.querySelector(".product-infos  > .product-quantity");
  let description = element.querySelector(".product-describe");
  let images = element.querySelector("div > .product-images");

  // Custom element of sub form
  element.setAttribute("id", `product-${index}`);

  title.textContent = `Product ${index}`;

  removeProductButton.innerHTML = `<div onclick="removeProduct('product-${index}')"
                                        class="remove-product p-1.5 h-max w-max bg-red-600 hover:bg-red-600/80 leading-none text-lg text-white rounded cursor-pointer transition ease-in-out duration-200">
                                        <i class="ri-close-fill"></i>
                                    </div>`;

  name.innerHTML = `<label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
                        for="product_name_${index}">
                        Product <i class="text-red-600">*</i>
                    </label>
                    <input
                        class="appearance-none block w-full bg-white text-gray-700 border border-gray-300 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-blue-green"
                        id="product_name_${index}" name="product_name_${index}" type="text" placeholder="Product name" required>`;

  quantity.innerHTML = `<label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
                            for="quantity_${index}">
                            Quantity <i class="text-red-600">*</i>
                        </label>
                        <input
                            class="appearance-none block w-full bg-white text-gray-700 border border-gray-300 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-blue-green"
                            id="quantity_${index}" name="quantity_${index}" value="1" type="number" min="1" placeholder="" required>`;

  description.innerHTML = `<label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
                                for="product_description_${index}">
                                Description <i class="text-red-600">*</i>
                            </label>
                            <textarea id="product_description_${index}" name="product_description_${index}" rows="3"
                                placeholder="Additional information of product here" required
                                class="block w-full rounded border border-gray-300 text-gray-700 placeholder:text-gray-400 leading-normal py-3 px-4 mb-4 focus:bg-white focus:border-blue-green"></textarea>`;

  images.innerHTML = `<div class="w-full md:w-1/2 px-3 mb-6">
                        <input type="file" class="r-only" name="product_picture_${index}_1"
                               accept="image/*" data-show-upload="true"
                               data-show-caption="true" data-show-preview="true"
                               id="product_picture_${index}_1" onchange="onAddPic(this)">
                        </div>
                        <div class="w-full md:w-1/2 px-3 mb-6">
                            <input type="file" class="r-only" name="product_picture_${index}_2"
                               accept="image/*" data-show-upload="true"
                               data-show-caption="true" data-show-preview="true"
                               id="product_picture_${index}_2" onchange="onAddPic(this)">
                        </div>
                        <div class="w-full md:w-1/2 px-3 mb-6">
                            <input type="file" class="r-only" name="product_picture_${index}_3"
                               accept="image/*" data-show-upload="true"
                               data-show-caption="true" data-show-preview="true"
                               id="product_picture_${index}_3" onchange="onAddPic(this)">
                        </div>
                        <div class="w-full md:w-1/2 px-3 mb-2 md:mb-0">
                            <input type="file" class="r-only" name="product_picture_${index}_4"
                               accept="image/*" data-show-upload="true"
                               data-show-caption="true" data-show-preview="true"
                               id="product_picture_${index}_4" onchange="onAddPic(this)">
                        </div>`;

  productList.appendChild(element);
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