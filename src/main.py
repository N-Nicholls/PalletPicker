import random

class Pallet:
    def __init__(self, pallet_id):
        self.skus = {}
        self.pallet_id = pallet_id
    
    def printPallet(self):
        print(f"Current Pallet #{self.pallet_id}: Total Toilets's: {sum([self.skus[key] for key in self.skus]):03d}")
        for key in self.skus:
            print(f"SKU: {key:03d} || Quantity: {self.skus[key]:02d}")

    def hasFourSkus(self):
        return len(self.skus) >= 4
    
    def totalToilets(self):
        return sum(self.skus.values())
    
    def add_sku(self, sku, quantity):
        if sku in self.skus:
            self.skus[sku] += quantity
        else:
            self.skus[sku] = quantity

class Toilet:
    def __init__(self, sku, pop, qnt):
        self.sku = sku
        self.popularity = pop
        self.max_quantity = qnt
        self.quantity = self.max_quantity


class Shelf:
    def __init__(self):
        self.shelf = []
        self.overhead = []
        toiletNames = []
        self.pallets = []


        for _ in range(random.randint(8,10)):
            
            # names next toilet
            if toiletNames is not None:
                toiletName = random.randint(0, 999)
                while toiletName in toiletNames:
                    toiletName = random.randint(0, 999)
            toiletNames.append(toiletName)

            # Find the popularity of the toilet
            value = random.randint(1, 10)
            if value == 10: # Popular Toilet, 50% sell rate per week
                quantity = 10
                popularity = quantity*0.5 / 7
            elif value > 7 and value < 10: # Semi-Popular Toilet, 30% sell rate per week
                quantity = random.randint(5, 10)
                popularity = quantity*0.3 / 7
            elif value <= 7: # Unpopular Toilet, 20% sell rate per week
                quantity = random.randint(3, 5)
                popularity = quantity*0.2 / 7
            self.shelf.append(Toilet(toiletName, popularity, quantity))

    def printShelf(self):
        print(f"Current Shelf: Total Sku's: {len(self.shelf):02d} Total Toilets: {sum([toilet.quantity for toilet in self.shelf]):03d}/" + str(sum([toilet.max_quantity for toilet in self.shelf])))
        for toilet in self.shelf:
            hashes = ""
            for _ in range(toilet.quantity):
                hashes += "#"
            for _ in range(toilet.max_quantity - toilet.quantity):
                hashes += "O"
            print(f"SKU: {toilet.sku:03d}, Popularity: {toilet.popularity:.2f}, Quantity: {toilet.quantity:02d}/{toilet.max_quantity:02d} || {hashes}")

    def newDay(self):
        for toilet in self.shelf:
            if random.randint(0, 100) < toilet.popularity*100 and toilet.quantity > 0:
                toilet.quantity -= 1

    def getItemsNeeded(self):

        items = {}
        for item in self.shelf:
            if item.quantity < item.max_quantity:
                value = item.max_quantity - item.quantity
                items[item.sku] = value
        print("Items Needed:", items, " Total Items:", sum(items.values()))

        items_needed = {}
        for items in self.shelf:
            if items.quantity < items.max_quantity:
                value = items.max_quantity - items.quantity
                value += random.choice([-1, -1, -2, 0, 0, 0, 0, 0, 0, 1, 1, 2, 3])
                if value > 0:
                    items_needed[items.sku] = value
            else:
                value = random.choice([0, 0, 0, 0, 0, 0, 0, 1, 1, 2])
                if value > 0:
                    items_needed[items.sku] = value
        return items_needed

    def populatePallets(self, items_needed):   

        print("Items Ordered:", items_needed, " Total Items:", sum(items_needed.values()))
        pallet_number = 1
        items_left = sum(items_needed.values())
        pallets = [Pallet(pallet_number)]  # Start with an initial empty pallet
        pallet_number += 1

        while items_left > 0:
            chosen = random.choice(list(items_needed.keys()))
            if items_needed[chosen] <= 0:
                continue  # Skip empty SKUs

            chosenAmt = random.randint(1, items_needed[chosen])
            items_needed[chosen] -= chosenAmt
            items_left -= chosenAmt

            for pallet in pallets:
                if pallet.totalToilets() + chosenAmt <= 5:  # Check if pallet can hold more items
                    if chosen in pallet.skus or not pallet.hasFourSkus():
                        pallet.add_sku(chosen, chosenAmt)
                        break
            else:  # No break means no pallet could hold it, so we need a new pallet
                new_pallet = Pallet(pallet_number)
                new_pallet.add_sku(chosen, chosenAmt)
                pallets.append(new_pallet)
                pallet_number += 1

        
        # Printing the pallets for debugging
        for idx, pallet in enumerate(pallets):
            print(f"Pallet {pallet.pallet_id}: {pallet.skus}")
        
        return pallets

    def calculateRestockingProgressively(self, pallet_order):
        print("\nOrder: ", end=" ")
        for pallet in pallet_order:
            print(pallet.pallet_id, end=" ")
        print()
        
        cumulative_items_stocked = 0
        cumulative_cost = 0
        up_cost = 0
        down_cost = 0
        items_needed = self.getItemsNeeded()

        results = []

        for i, pallet in enumerate(pallet_order, start=1):
            print(f"\nAfter Bringing down Pallet {pallet.pallet_id}:")
            pallet_items_stocked = 0
            pallet_items_left = {}

            # Cost for taking down the pallet
            cumulative_cost += 1
            down_cost += 1

            for sku, quantity in pallet.skus.items():
                if sku in items_needed and items_needed[sku] > 0:
                    # Ensure you don't stock more than needed
                    stock_amount = min(quantity, items_needed[sku])
                    items_needed[sku] -= stock_amount
                    cumulative_items_stocked += stock_amount
                    pallet_items_stocked += stock_amount

                    # Track any leftover items in the pallet
                    if quantity > stock_amount:
                        pallet_items_left[sku] = quantity - stock_amount

            # If the pallet is not fully used, it needs to be put back up
            if pallet_items_left:
                cumulative_cost += 1  # Cost for putting up a pallet
                up_cost += 1

            results.append((cumulative_items_stocked, cumulative_cost))
            print(f"  Cumulative items stocked: {cumulative_items_stocked}")
            print(f"  Cumulative cost: {cumulative_cost} || Down cost: {down_cost} || Up cost: {up_cost}")

        return results

if __name__ == '__main__':
    shelf = Shelf()
    shelf.printShelf()
    for _ in range(7): 
        shelf.newDay()
        shelf.printShelf()
    shelf.pallets = shelf.populatePallets(shelf.getItemsNeeded())

    pallet_order = shelf.pallets
    results = shelf.calculateRestockingProgressively(pallet_order)
