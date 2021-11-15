### TODO

Frontend
- Display 
- [X] Filter by Rank
- [X] Filter by Price
- [ ] Link to Asset Modal (TLD/:project/:drop/:serial)
    - [ ] Link to tweet
- [ ] Add Selected Chain Indicator
- [ ] Add Link To cnft.io
- [ ] Dynamically Include and Exclude Fields When Sending Requests
- [X] Add Search by ID
- [X] Flesh out Distribution Interactivity
    - [X] Fix Null/None trait options
    - [X] Collapse Automatically on select for traits that do not map to lists
- [X] Add Modal for Each Asset
- [X] Add Rarity Calculation
- [X] Migrate To Vuex
- ~~Add Close Button To AssetModal~~

Backend
- [ ] Factor Out Distribution
    - [ ] Create Category Model
        - name
        - traits []
        - trait count {}
        - trait rarity_score {}
        - trait custom_score {}
        - trait normalized_score {}
        - trait floor {}
        - foreign key: Collection()
    - Serialize Collection.categories
- [X] Periodic Price Fetching
- [ ] Improve Price Fetching Speed
- [ ] Streamline Project Listing
- [ ] Fetch Individual Asset by serial (Asset Modal)
- [X] Add Distribution as Collection Field
