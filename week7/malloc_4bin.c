//
// >>>> malloc challenge! <<<<
//
// Your task is to improve utilization and speed of the following malloc
// implementation.
// Initial implementation is the same as the one implemented in simple_malloc.c.
// For the detailed explanation, please refer to simple_malloc.c.

#include <assert.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//
// Interfaces to get memory pages from OS
//

void *mmap_from_system(size_t size);
void munmap_to_system(void *ptr, size_t size);

//
// Struct definitions
//

typedef struct my_metadata_t {
  size_t size;
  struct my_metadata_t *next;
} my_metadata_t;

typedef struct my_heap_t {
  my_metadata_t *bins[4];   //4つのbinの先頭アドレス
  /*my_metadata_t dummy;  Free binならダミーいらない？*/
} my_heap_t;

//
// Static variables (DO NOT ADD ANOTHER STATIC VARIABLES!)
//
my_heap_t my_heap;

//
// Helper functions (feel free to add/remove/edit!)
//
//空きリストの先頭に挿入する関数
void my_add_to_free_list(my_metadata_t *metadata) {
  assert(!metadata->next);
  int new_size = metadata->size;
  int insert_bin_num  = new_size / 1000;

  metadata->next = my_heap.bins[new_size];    /*今のbin[i]の先頭をmetadataの次に*/
  my_heap.bins[new_size] = metadata;  /*先頭を今解放したものに*/

}


void my_remove_from_free_list(my_metadata_t *metadata, my_metadata_t *prev, int bin_index) { /*解放するメモリがどのbinにあったかを引数で与える*/
  if (prev){
    prev->next = metadata->next;
  }else{
    my_heap.bins[bin_index] = metadata->next;
  }
  metadata->next = NULL;
}

//
// Interfaces of malloc (DO NOT RENAME FOLLOWING FUNCTIONS!)
//

// This is called at the beginning of each challenge.
void my_initialize() {
  for (int i = 0; i < 4; ++i){
    my_heap.bins[i] = NULL;     //それぞれのbinの先頭にNULLをおく
  }
}

// my_malloc() is called every time an object is allocated.
// |size| is guaranteed to be a multiple of 8 bytes and meets 8 <= |size| <=
// 4000. You are not allowed to use any library functions other than
// mmap_from_system() / munmap_to_system().
void *my_malloc(size_t size) {
  //Free list bin　
  //四つに分けているのでどのbinにあるか探す
  
  int bin_num = size / 1000;     /*どのbinにあるか*/
  my_metadata_t *metadata = NULL;  /*先頭を設定*/
  my_metadata_t *prev = NULL;
  int match_bin_index = -1; /*最小のフリースペースがどのbinにあるか*/

  for (int i = bin_num; i < 4; ++i){  /*want_sizeのbinからその上のbinまでを確認*/
    metadata = my_heap.bins[i];  /*先頭を設定*/
    

    size_t min_size = 4096;  /*初めは一番大きいメモリを設定*/
    my_metadata_t *min_metadata = NULL; /*最小部分の先頭のポインタ*/
    my_metadata_t *min_prev = NULL; /*上の一個前のノード*/
    

    while (metadata && metadata->size < size) {
      /*Best-fitの実装*/
      if(metadata->size >= size && metadata->size < min_size){ 
        min_size = metadata->size;
        min_metadata = metadata;
        min_prev = prev;
      }
      prev = metadata;
      metadata = metadata->next; 
    }

    if (min_metadata != NULL){  /*今見てるbinで欲しいサイズのものが一つでもあったとき*/
      match_bin_index = i;
      prev = min_prev;
      metadata = min_metadata;
      break; /*そのbinで最小なら次のbinは見なくていい*/
    }
  }
  // now, metadata points to the first free slot
  // and prev is the previous entry.

  if (!metadata) {
    // There was no free slot available. We need to request a new memory region
    // from the system by calling mmap_from_system().
    //
    //     | metadata | free slot |
    //     ^
    //     metadata
    //     <---------------------->
    //            buffer_size
    size_t buffer_size = 4096;
    my_metadata_t *metadata = (my_metadata_t *)mmap_from_system(buffer_size);
    metadata->size = buffer_size - sizeof(my_metadata_t);
    metadata->next = NULL;
    // Add the memory region to the free list.
    my_add_to_free_list(metadata);
    // Now, try my_malloc() again. This should succeed.
    return my_malloc(size);
  }
  
  // |ptr| is the beginning of the allocated object.
  //
  // ... | metadata | object | ...
  //     ^          ^
  //     metadata   ptr
  void *ptr = metadata + 1;
  size_t remaining_size = metadata->size - size;
  metadata->size = size;
  // フリーなリストからmallocしたものを消す
  if(metadata && match_bin_index != -1){   /*該当するmetadataがなかったときは以下の操作はいらない*/ 
    my_remove_from_free_list(metadata, prev, match_bin_index);
  }
  if (remaining_size > sizeof(my_metadata_t)) {
    // Create a new metadata for the remaining free slot.
    //
    // ... | metadata | object | metadata | free slot | ...
    //     ^          ^        ^
    //     metadata   ptr      new_metadata
    //                 <------><---------------------->
    //                   size       remaining size
    my_metadata_t *new_metadata = (my_metadata_t *)((char *)ptr + size);
    new_metadata->size = remaining_size - sizeof(my_metadata_t);
    new_metadata->next = NULL;
    // 残ったフリー部分をフリーリストに入れ直す
    my_add_to_free_list(new_metadata);
  }
  return ptr;
}

// This is called every time an object is freed.  You are not allowed to
// use any library functions other than mmap_from_system / munmap_to_system.
void my_free(void *ptr) {
  // Look up the metadata. The metadata is placed just prior to the object.
  //
  // ... | metadata | object | ...
  //     ^          ^
  //     metadata   ptr
  my_metadata_t *metadata = (my_metadata_t *)ptr - 1;
  // Add the free slot to the free list.
  my_add_to_free_list(metadata);
  
}

// This is called at the end of each challenge.
void my_finalize() {
  // Nothing is here for now.
  // feel free to add something if you want!
}

void test() {
  // Implement here!
  assert(1 == 1); /* 1 is 1. That's always true! (You can remove this.) */
}
