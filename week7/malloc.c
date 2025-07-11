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
#define BINS_NUM 4

typedef struct my_metadata_t {
  size_t size;
  struct my_metadata_t *next;
} my_metadata_t;

typedef struct my_heap_t {
  my_metadata_t *free_head;   //4つのbinの先頭アドレス
  my_metadata_t dummy;  
} my_heap_t;

my_heap_t heaps[BINS_NUM];
//
// Static variables (DO NOT ADD ANOTHER STATIC VARIABLES!)
//
my_heap_t my_heap;

//
// サイズがどのbinに入るかを教えてくれる補助関数
int get_bin_index(size_t size) {
  int bin = (size - 1) / 1000;
  if (bin >= BINS_NUM) bin = BINS_NUM - 1;
  return bin;
}
//
//空きリストの先頭に挿入する関数
void my_add_to_free_list(my_metadata_t *metadata, int bin_index) {
  assert(metadata && !metadata->next);
  metadata->next = heaps[bin_index].free_head;    /*入るbinの先頭を今のnextに*/
  heaps[bin_index].free_head = metadata;  /*先頭を新しくフリーリストに追加したものに*/
}

//空きリストから削除する関数
void my_remove_from_free_list(my_metadata_t *metadata, my_metadata_t *prev, int bin_index) { /*解放するメモリがどのbinにあったかを引数で与える*/
  if (prev){  /*metadataの場所が中間*/
    prev->next = metadata->next;  
  }else{  /*metadataの場所が先頭*/
    heaps[bin_index].free_head = metadata->next;
  }
  metadata->next = NULL;
}

//
// Interfaces of malloc (DO NOT RENAME FOLLOWING FUNCTIONS!)
//

// This is called at the beginning of each challenge.
void my_initialize() {
  for (int i = 0; i < BINS_NUM; ++i) {
    heaps[i].dummy.size = 0;
    heaps[i].dummy.next = NULL;
    heaps[i].free_head = &heaps[i].dummy;  /*dummy を free list の先頭に*/
  }
}

// 各binごとのmallocの処理を行う　ー＞　forやifの節約

void *my_malloc_on_bin(size_t size, int bin_index) {
  // printf("[INFO] Called my_malloc_on_bin: size=%zu, bin_index=%d\n", size, bin_index);
  my_metadata_t *prev = &heaps[bin_index].dummy;
  my_metadata_t *metadata = prev->next;  /*先頭を設定*/

  // Best Fit用の初期設定　
  size_t min_size = 5000;  /*初めは一番大きいメモリを設定*/
  my_metadata_t *min_metadata = NULL; /*最小部分の先頭のポインタ*/
  my_metadata_t *min_prev = NULL; /*上の一個前のノード*/
  int match_bin_index = -1; /*見つかったbinを保存しておく*/

  for (int i = bin_index; i < BINS_NUM; ++i){  /*want_sizeのbinからその上のbinまでを確認*/
    prev = &heaps[i].dummy;
    metadata = prev->next;

    while (metadata) {
      /*Best-fitの実装*/
      if(metadata->size >= size && metadata->size < min_size){ 
        min_size = metadata->size;
        min_metadata = metadata;
        min_prev = prev;
      }
      prev = metadata;
      metadata = metadata->next; 
    }

    if (min_metadata){  /*今見てるbinで欲しいサイズのものが一つでもあったとき*/
      match_bin_index = i;
      // prev = min_prev;
      // metadata = min_metadata;
      break; /*そのbinで最小なら次のbinは見なくていい*/
    }
  }
  // now, metadata points to the first free slot
  // and prev is the previous entry.

  if (!min_metadata) {
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
    int new_bin_index = get_bin_index(metadata->size);
    my_add_to_free_list(metadata, new_bin_index);
    
    return my_malloc_on_bin(size, bin_index);
  }
  // フリースロットからの削除
  metadata = min_metadata;
  prev = min_prev;
  my_remove_from_free_list(metadata, prev, match_bin_index);
  metadata->size = size;
  
  // |ptr| is the beginning of the allocated object.
  //
  // ... | metadata | object | ...
  //     ^          ^
  //     metadata   ptr
  void *ptr = metadata + 1;
  size_t remaining_size = metadata->size - size;
  
  // 残ったサイズがフリースロットに戻すに値するか
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
    int new_bin = get_bin_index(new_metadata->size);
    my_add_to_free_list(new_metadata, new_bin);
    metadata->size = size;
  
  }
  return ptr;
}

// my_malloc() is called every time an object is allocated.
// |size| is guaranteed to be a multiple of 8 bytes and meets 8 <= |size| <=
// 4000. You are not allowed to use any library functions other than
// mmap_from_system() / munmap_to_system().
void *my_malloc(size_t size){
  int bin_index = get_bin_index(size);   //四つに分けているのでどのbinにあるか探す
  return my_malloc_on_bin(size, bin_index);
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
  int bin_index = get_bin_index(metadata->size);
  my_add_to_free_list(metadata, bin_index);
  
}

// This is called at the end of each challenge.
void my_finalize() {

}

void test() {
  // Implement here!
  assert(1 == 1); /* 1 is 1. That's always true! (You can remove this.) */
}
