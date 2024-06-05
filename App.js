import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
    const [categories, setCategories] = useState([]);
    const [subCategories, setSubCategories] = useState([]);
    const [products, setProducts] = useState([]);
    const [selectedCategory, setSelectedCategory] = useState('');
    const [selectedSubCategory, setSelectedSubCategory] = useState('');

    useEffect(() => {
        axios.get('/api/products/categories')
            .then(response => setCategories(response.data))
            .catch(error => console.error('Error fetching categories:', error));
    }, []);

    const handleCategorySelect = (category) => {
        setSelectedCategory(category);
        axios.get(`/api/products/subcategories?category=${category}`)
            .then(response => setSubCategories(response.data))
            .catch(error => console.error('Error fetching subcategories:', error));
    };

    const handleSubCategorySelect = (subCategory) => {
        setSelectedSubCategory(subCategory);
        axios.get(`/api/products/items?category=${selectedCategory}&subCategory=${subCategory}`)
            .then(response => setProducts(response.data))
            .catch(error => console.error('Error fetching products:', error));
    };

    return (
        <div>
            <h1>Stationery Shop</h1>
            <div>
                <h2>Categories</h2>
                <ul>
                    {categories.map(category => (
                        <li key={category} onClick={() => handleCategorySelect(category)}>
                            {category}
                        </li>
                    ))}
                </ul>
            </div>
            {subCategories.length > 0 && (
                <div>
                    <h2>Subcategories</h2>
                    <ul>
                        {subCategories.map(subCategory => (
                            <li key={subCategory} onClick={() => handleSubCategorySelect(subCategory)}>
                                {subCategory}
                            </li>
                        ))}
                    </ul>
                </div>
            )}
            {products.length > 0 && (
                <div>
                    <h2>Products</h2>
                    <ul>
                        {products.map(product => (
                            <li key={product.id}>
                                <h3>{product.productName}</h3>
                                <p>Price: ${product.price}</p>
                                <p>Quantity: {product.quantity}</p>
                                <img src={`data:image/jpeg;base64,${product.image}`} alt={product.productName} />
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
}

export default App;
