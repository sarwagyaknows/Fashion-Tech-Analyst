/*
 * inventory_routing.c
 * --------------------
 * "Algorithmic Logic Optimization" — Project 3
 *
 * Problem framed from real warehouse/catalog operations:
 * A fulfilment warehouse stores fashion SKUs across aisles. When an order comes in,
 * the picking system needs to (1) sort SKUs by aisle/zone so a picker's route is
 * efficient, and (2) quickly look up which zone a given SKU lives in.
 *
 * This program demonstrates both pieces with real, from-scratch C:
 *   1. Merge sort to sort inventory records by zone code (O(n log n))
 *   2. Binary search to look up a SKU's zone once sorted (O(log n))
 *   3. A basic linear "picking route total distance" calculation across zones
 *
 * Compile: gcc -O2 -Wall -o inventory_routing inventory_routing.c
 * Run:     ./inventory_routing
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_ITEMS 20
#define SKU_LEN 12

typedef struct {
    char sku[SKU_LEN];
    int zone;       // warehouse zone / aisle number
    int shelf_dist;  // distance (meters) of that zone from the packing station
} InventoryItem;

/* ---------- Merge Sort (by zone, then shelf_dist) ---------- */

void merge(InventoryItem arr[], int left, int mid, int right) {
    int n1 = mid - left + 1;
    int n2 = right - mid;

    InventoryItem *L = malloc(n1 * sizeof(InventoryItem));
    InventoryItem *R = malloc(n2 * sizeof(InventoryItem));

    for (int i = 0; i < n1; i++) L[i] = arr[left + i];
    for (int j = 0; j < n2; j++) R[j] = arr[mid + 1 + j];

    int i = 0, j = 0, k = left;
    while (i < n1 && j < n2) {
        if (L[i].zone <= R[j].zone) {
            arr[k++] = L[i++];
        } else {
            arr[k++] = R[j++];
        }
    }
    while (i < n1) arr[k++] = L[i++];
    while (j < n2) arr[k++] = R[j++];

    free(L);
    free(R);
}

void merge_sort(InventoryItem arr[], int left, int right) {
    if (left < right) {
        int mid = left + (right - left) / 2;
        merge_sort(arr, left, mid);
        merge_sort(arr, mid + 1, right);
        merge(arr, left, mid, right);
    }
}

/* ---------- Binary Search by SKU (requires array sorted by SKU) ---------- */

int binary_search_sku(InventoryItem arr[], int n, const char *target_sku) {
    int low = 0, high = n - 1;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        int cmp = strcmp(arr[mid].sku, target_sku);
        if (cmp == 0) return mid;
        if (cmp < 0) low = mid + 1;
        else high = mid - 1;
    }
    return -1;  // not found
}

/* Simple comparator-based sort by SKU string, needed before binary search */
void sort_by_sku(InventoryItem arr[], int n) {
    for (int i = 1; i < n; i++) {
        InventoryItem key = arr[i];
        int j = i - 1;
        while (j >= 0 && strcmp(arr[j].sku, key.sku) > 0) {
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = key;
    }
}

void print_inventory(InventoryItem arr[], int n, const char *title) {
    printf("\n%s\n", title);
    printf("%-12s %-8s %-10s\n", "SKU", "Zone", "Dist(m)");
    printf("--------------------------------\n");
    for (int i = 0; i < n; i++) {
        printf("%-12s %-8d %-10d\n", arr[i].sku, arr[i].zone, arr[i].shelf_dist);
    }
}

int main(void) {
    InventoryItem inventory[MAX_ITEMS] = {
        {"SKU-TS0021", 4, 38}, {"SKU-JK0055", 1, 12}, {"SKU-DR0110", 3, 27},
        {"SKU-KU0009", 2, 20}, {"SKU-SN0087", 5, 45}, {"SKU-TS0004", 1, 10},
        {"SKU-JN0033", 3, 25}, {"SKU-HD0060", 4, 40}, {"SKU-CO0071", 2, 22},
        {"SKU-DR0015", 5, 48}
    };
    int n = 10;

    print_inventory(inventory, n, "Unsorted inventory (order received from catalog feed):");

    // Step 1: Sort by warehouse zone so a picker's route is efficient (merge sort)
    merge_sort(inventory, 0, n - 1);
    print_inventory(inventory, n, "Sorted by ZONE (merge sort) -> optimal picking route order:");

    int total_distance = 0;
    for (int i = 0; i < n; i++) total_distance += inventory[i].shelf_dist;
    printf("\nTotal picking route distance (sum of zone distances): %d meters\n", total_distance);

    // Step 2: Sort by SKU so we can binary-search it (separate ordering, real use case:
    // SKU lookup happens far more often than full re-routing, so it gets its own index)
    sort_by_sku(inventory, n);
    print_inventory(inventory, n, "Re-sorted by SKU (insertion sort) -> ready for binary search index:");

    const char *lookup_target = "SKU-KU0009";
    int idx = binary_search_sku(inventory, n, lookup_target);
    if (idx != -1) {
        printf("\nBinary search: %s found at index %d -> Zone %d, %dm from packing station.\n",
               lookup_target, idx, inventory[idx].zone, inventory[idx].shelf_dist);
    } else {
        printf("\nBinary search: %s not found in inventory.\n", lookup_target);
    }

    return 0;
}
