import pickle 

entities = {
    "authentication",
    "employees",
    "pays" 
}

class Query():
    
    def __init__(self, entity_name=None):
        
        if entity_name is None:
            raise ValueError("Missing value: Class Object")
        elif entity_name not in entities:
            raise ValueError("Object entity is not supported") 
        
        self.entity_name = entity_name
        self.results = None

    @property
    def fetch_records(self):

        # Open and read file
        entity_file_directory = "common/entities/{}.txt".format(self.entity_name)

        with open(entity_file_directory) as file:
            # Split lines into list and remove all comments
            data = [line.strip("\n").split("\t\t") for line in file if "#" not in line]
            file.close()
        
        # Separate key and records
        keys = data[0]
        records = data[1:]
        
        # Format records into JSON with their corresponding keys
        return [dict(zip(keys, record)) for record in records]
    
    def get(self):
        return self.results

    # Returns records that match the values provided
    def select(self):
        self.results = self.fetch_records
        return self


    def where(self, **kwargs):
        
        if kwargs is None:
            raise ValueError("Must provide arguments to filter results")
        
        if self.results is None or len(self.results) == 0:
            return self

        argument_keys = list(kwargs.keys())
        argument_values = list(kwargs.values())

        # Get the first dictionary from the results list
        first_result = self.results[0]

        # Check to see if any of the search parameters aren't valid
        for key in argument_keys:
            if key not in first_result:
                raise KeyError("Keyname {} not found in record".format(key))

        # Filter results list down into a list of lists containing only values specified from the arguments  
        argument_value_only_list = [[record[key] for key in argument_keys] for record in self.results]

        # Collect the indicies of the lists that match the argument values
        filtered_results_indicies = []

        for index in range(len(argument_value_only_list)):
            if argument_value_only_list[index] == argument_values:
                filtered_results_indicies.append(index)

        # Collect the fitlered results
        filtered_results = [self.results[index] for index in filtered_results_indicies]  
        
        self.results = filtered_results

        return self

    def update(self, **kwargs):
        
        if kwargs is None:
            raise ValueError("Must provide arguments to update")

        if self.results is None or len(self.results) == 0:
            return self

        argument_keys = list(kwargs.keys())

        # Get the first dictionary from the results list
        first_result = self.results[0]

        # Check to see if any of the search parameters aren't valid
        for key in argument_keys:
            if key not in first_result:
                raise KeyError("Keyname {} not found in record".format(key))

        original_results = self.fetch_records

        indicies = [
            original_results.index(record) 
            for 
            record 
            in 
            self.results]

        for record in self.results:
            for key in kwargs:
                record[key] = kwargs[key]

        for index in indicies:
            original_results[index] = self.results.pop(0)

        with open("common/entities/{}.txt".format(self.entity_name), 'w') as file:
            keys = list(original_results[0].keys())
            
            records = [
                "\t\t".join(list(record.values())) + "\n" 
                for 
                record 
                in 
                original_results]
            
            file_data = ["\t\t".join(keys) + "\n"] + records            
            
            file.writelines(file_data)

            file.close()

        return True


        