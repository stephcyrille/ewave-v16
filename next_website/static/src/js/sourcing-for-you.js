// Dynamic Field Creation

const productList = document.querySelector("#products-list");
const productForm = productList.querySelector(".product-form");
const addProductButton = document.querySelector("#add-product");
let size = productList.childElementCount;

addProductButton.addEventListener("click", addProduct);

/**
 * removeProduct: the function remove a form for a new product
 */

function removeProduct(index) {
  let element = document.getElementById(index);
  element.remove();
}

/**
 * addProduct: the function add a form for a new product
 */
function addProduct() {
  size++;

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
                        for="product-${index}-name">
                        Product <i class="text-red-600">*</i>
                    </label>
                    <input
                        class="appearance-none block w-full bg-white text-gray-700 border border-gray-300 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-blue-green"
                        id="product-${index}-name" name="product-${index}-name" type="text" placeholder="Product name" required>`;

  quantity.innerHTML = `<label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
                            for="product-${index}-quantity">
                            Quantity <i class="text-red-600">*</i>
                        </label>
                        <input
                            class="appearance-none block w-full bg-white text-gray-700 border border-gray-300 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-blue-green"
                            id="product-${index}-quantity" name="product-${index}-quantity" value="1" type="number" min="1" placeholder="" required>`;

  description.innerHTML = `<label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
                                for="product-${index}-description">
                                Description <i class="text-red-600">*</i>
                            </label>
                            <textarea id="product-${index}-description" name="product-${index}-description" rows="3"
                                placeholder="Additional information of product here" required
                                class="block w-full rounded border border-gray-300 text-gray-700 placeholder:text-gray-400 leading-normal py-3 px-4 mb-4 focus:bg-white focus:border-blue-green"></textarea>`;

  images.innerHTML = `<div class="w-full md:w-1/2 px-3 mb-6">
                            <input id="product-${index}-file-1" name="product-${index}-file-1" type="file" class="r-only">
                        </div>
                        <div class="w-full md:w-1/2 px-3 mb-6">
                            <input id="product-${index}-file-2" name="product-${index}-file-2" type="file" class="r-only">
                        </div>
                        <div class="w-full md:w-1/2 px-3 mb-6">
                            <input id="product-${index}-file-3" name="product-${index}-file-3" type="file" class="r-only">
                        </div>
                        <div class="w-full md:w-1/2 px-3 mb-2 md:mb-0">
                            <input id="product-${index}-file-4" name="product-${index}-file-4" type="file" class="r-only">
                        </div>`;

  productList.appendChild(element);
}
