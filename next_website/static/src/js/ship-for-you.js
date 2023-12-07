// Dynamic Field Creation

const packList = document.querySelector("#pack-list");
const packForm = packList.querySelector(".pack-form");
const addPackButton = document.querySelector("#add-pack");
let size = packList.childElementCount;

addPackButton.addEventListener("click", addPack);

/**
 * removePack: the function remove a form for a new pack
 */

function removePack(index) {
  let element = document.getElementById(index);
  element.remove();
}

/**
 * addPack: the function add a form for a new pack
 */
function addPack() {
  size++;

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

  name.innerHTML = `<label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="pack-${index}-name">
                        Name <i class="text-red-600">*</i>
                    </label>
                    <input class="appearance-none block w-full bg-white text-gray-700 text-sm border border-gray-300 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-blue-green"
                        id="pack-${index}-name" name="pack-${index}-name" type="text" placeholder="pack name" required>`;

  material.innerHTML = `<label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="pack-${index}-material">
                            Material <i class="text-red-600">*</i>
                        </label>
                        <input class="appearance-none block w-full bg-white text-gray-700 text-sm border border-gray-300 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-blue-green"
                            id="pack-${index}-material" name="pack-${index}-material" type="text" placeholder="Other" required>`;

  quantity.innerHTML = `<label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="pack-${index}-quantity">
                            Quantity <i class="text-red-600">*</i>
                        </label>
                        <input class="appearance-none block w-full bg-white text-gray-700 text-sm border border-gray-300 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-blue-green"
                            id="pack-${index}-quantity" name="pack-${index}-quantity" value="1" step="1" type="number" min="1" placeholder="" required>`;

  weight.innerHTML = `<label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="pack-${index}-weight">
                            Weight (Kg) <i class="text-red-600">*</i>
                        </label>
                        <input class="appearance-none block w-full bg-white text-gray-700 text-sm border border-gray-300 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-blue-green"
                            id="pack-${index}-weight" name="pack-${index}-weight" value="1.00" step="0.01" type="number" min="0.01" placeholder="" required>`;

  capacity.innerHTML = `<label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="pack-${index}-capacity">
                            Capicity (m3) <i class="text-red-600">*</i>
                        </label>
                        <input class="appearance-none block w-full bg-white text-gray-700 text-sm border border-gray-300 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-blue-green"
                            id="pack-${index}-capacity" name="pack-${index}-capacity" value="1.00" step="0.01" type="number" min="0.01" placeholder="" required>`;

  price.innerHTML = `<label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="pack-${index}-price">
                        Estimated price <i class="text-red-600">*</i>
                    </label>
                    <input class="appearance-none block w-full bg-white text-gray-700 text-sm border border-gray-300 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-blue-green"
                        id="pack-${index}-price" name="pack-${index}-price" value="1.00" step="0.01" type="number" min="0.01" placeholder="" required>`;

  packList.appendChild(element);
}
