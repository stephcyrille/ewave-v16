// Dynamic Field Creation

const packList = document.querySelector("#pack-list");
const packForm = packList.querySelector(".pack-form");
const addPackButton = document.querySelector("#add-pack");
//let size = packList.childElementCount;

addPackButton.addEventListener("click", addPack);

/**
  * Increase the counter of products when we trigger on add button action
*/

 // Product increment
var size = 1;
var tab_counter = 1;


/**
 * removePack: the function remove a form for a new pack
 */
function removePack(index) {
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
 * addPack: the function add a form for a new pack
 */
function addPack() {
  size++;
  tab_counter ++;

  document.getElementsByName("product_counter")[0].value = tab_counter;

  let element = packForm.cloneNode(true);
  let index = size;

  //Get element of the sub form pack
  let title = element.querySelector("div > .pack-title");
  let removePackButton = element.querySelector("div > .remove-pack");
  let name = element.querySelector(".pack-infos > .pack-name");
  let material = element.querySelector(".pack-infos  > .pack-material");
  let quantity = element.querySelector(".pack-infos > .pack-quantity");
  let weight = element.querySelector(".pack-infos  > .pack-weight");
  let capacity = element.querySelector(".pack-infos > .pack-capacity");
  let price = element.querySelector(".pack-infos  > .pack-price");

  // Custom element of sub form
  element.setAttribute("id", `pack-${index}`);

  title.textContent = `Product ${index}`;

  removePackButton.innerHTML = `<div onclick="removePack('pack-${index}')"
                                        class="remove-pack p-1.5 h-max w-max bg-red-600 hover:bg-red-600/80 leading-none text-lg text-white rounded cursor-pointer transition ease-in-out duration-200">
                                        <i class="ri-close-fill"></i>
                                    </div>`;

  name.innerHTML = `<label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="product_name_${index}">
                        Name <i class="text-red-600">*</i>
                    </label>
                    <input class="appearance-none block w-full bg-white text-gray-700 text-sm border border-gray-300 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-blue-green"
                        id="product_name_${index}" name="product_name_${index}" type="text" placeholder="pack name" required>`;

  material.innerHTML = `<label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="product_material_${index}">
                            Material <i class="text-red-600">*</i>
                          </label>
                          <div class="relative">
                            <select class="block appearance-none  w-full bg-white border border-gray-300 text-gray-700 text-sm py-3 px-4 pr-8 mb-3 rounded leading-tight focus:outline-none focus:bg-white focus:border-blue-green"
                            id="product_material_${index}" name="product_material_${index}">
                              <option value="cosmetic">Cosmetic</option>
                              <option value="electronic">Electronic</option>
                              <option value="shoes">Shoes</option>
                              <option value="textile">Textile</option>
                              <option value="other">Other</option>
                            </select>
                            <div
                              class="pointer-events-none text-2xl absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
                              <i class="ri-arrow-down-s-fill" />
                            </div>
                          </div>`

  quantity.innerHTML = `<label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="pack-${index}-quantity">
                            Quantity <i class="text-red-600">*</i>
                        </label>
                        <input class="appearance-none block w-full bg-white text-gray-700 text-sm border border-gray-300 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-blue-green"
                            id="quantity_${index}" name="quantity_${index}" value="1" step="1" type="number" min="1" placeholder="" required>`;

  weight.innerHTML = `<label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="product_weight_${index}">
                            Weight (Kg) <i class="text-red-600">*</i>
                        </label>
                        <input class="appearance-none block w-full bg-white text-gray-700 text-sm border border-gray-300 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-blue-green"
                            id="product_weight_${index}-weight" name="product_weight_${index}" value="1.00" step="0.01" type="number" min="0.01" placeholder="" required>`;

  capacity.innerHTML = `<label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="pack-${index}-capacity">
                            Capicity (m3) <i class="text-red-600">*</i>
                        </label>
                        <input class="appearance-none block w-full bg-white text-gray-700 text-sm border border-gray-300 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-blue-green"
                            id="product_capacity_${index}" name="product_capacity_${index}" value="1.00" step="0.01" type="number" min="0.01" placeholder="" required>`;

  price.innerHTML = `<label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="product_price_${index}">
                        Estimated price <i class="text-red-600">*</i>
                    </label>
                    <input class="appearance-none block w-full bg-white text-gray-700 text-sm border border-gray-300 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-blue-green"
                        id="product_price_${index}" name="product_price_${index}" value="1.00" step="0.01" type="number" min="0.01" placeholder="" required>`;

  packList.appendChild(element);
}
