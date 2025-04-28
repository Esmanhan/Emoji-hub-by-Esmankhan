import React, { useState, useEffect } from 'react';

const SearchApp = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [emojiData, setEmojiData] = useState([]);
  const [filteredItems, setFilteredItems] = useState([]);

  // Загружаем данные с API
  useEffect(() => {
    fetch('https://emojihub.yurace.pro/api/all')
      .then(response => response.json())
      .then(data => {
        setEmojiData(data);
        setFilteredItems(data); // Изначально показываем все эмодзи
      })
      .catch(error => console.error('Error fetching emoji data:', error));
  }, []);

  // Обработчик поиска
  const handleSearch = () => {
    const filtered = emojiData.filter(item => {
      const matchesQuery = item.name.toLowerCase().includes(searchQuery.toLowerCase());
      const matchesCategory = selectedCategory ? item.category === selectedCategory : true;
      return matchesQuery && matchesCategory;
    });
    setFilteredItems(filtered);
  };

  return (
    <div>
      <form onSubmit={(e) => e.preventDefault()}>
        <input
          type="text"
          className="form-control"
          id="firstName"
          placeholder="Search"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          required
        />
        <select
          className="form-select"
          id="category"
          value={selectedCategory}
          onChange={(e) => setSelectedCategory(e.target.value)}
        >
          <option value="">Choose category</option>
          <option value="smileys-and-people">smileys-and-people</option>
          <option value="animals-and-nature">animals-and-nature</option>
          <option value="food-and-drink">food-and-drink</option>
          <option value="travel-and-places">travel-and-places</option>
          <option value="activities">activities</option>
          <option value="objects">objects</option>
          <option value="symbols">symbols</option>
          <option value="flags">flags</option>
        </select>
        <button className="btn-search" type="button" onClick={handleSearch}>
          Search
        </button>
      </form>

      <div>
        {filteredItems.length > 0 ? (
          <ul>
            {filteredItems.map((item, index) => (
              <li key={index}>
                <span>{item.character}</span> {item.name}
              </li>
            ))}
          </ul>
        ) : (
          <p>No results found</p>
        )}
      </div>
    </div>
  );
};

export default SearchApp;
