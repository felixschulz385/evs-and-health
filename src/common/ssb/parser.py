import pandas as pd
import json

def parse_jsonstat(json_data):
    """Parse JSON-stat format from SSB API to pandas DataFrame"""
    if isinstance(json_data, str):
        data = json.loads(json_data)
    else:
        data = json_data
    
    # Extract dimensions and their labels
    dimensions = data['dimension']
    dim_names = list(dimensions.keys())
    
    # Get dimension sizes and create index mapping
    sizes = data['size']
    values = data['value']
    
    # Create all combinations of dimension indices
    records = []
    total_combinations = 1
    for size in sizes:
        total_combinations *= size
    
    for i in range(total_combinations):
        record = {}
        temp_i = i
        
        # Calculate indices for each dimension
        for j, dim_name in enumerate(dim_names):
            dim_size = sizes[j]
            if j < len(sizes) - 1:
                next_size = 1
                for k in range(j + 1, len(sizes)):
                    next_size *= sizes[k]
                dim_index = temp_i // next_size
                temp_i = temp_i % next_size
            else:
                dim_index = temp_i
            
            # Get the actual value/label for this dimension
            dim_data = dimensions[dim_name]
            if 'category' in dim_data and 'index' in dim_data['category']:
                # Find the key for this index
                index_map = dim_data['category']['index']
                labels = dim_data['category']['label']
                
                # Find key by index value
                key = None
                for k, v in index_map.items():
                    if v == dim_index:
                        key = k
                        break
                
                if key and key in labels:
                    record[dim_name] = labels[key]
                else:
                    record[dim_name] = key or str(dim_index)
            else:
                record[dim_name] = str(dim_index)
        
        # Add the value
        record['value'] = values[i] if i < len(values) else None
        records.append(record)
    
    return pd.DataFrame(records)
