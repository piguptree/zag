#!/usr/bin/env python
# coding: utf-8

matrix=[list(".4..63..."),##专家
      list(".8.....26"),
      list("...1....."),
      list("1..6..4.."),
      list("3.7.....8"),
      list("....2..5."),
      list("...7..3.."),
      list("..4.5...."),
      list("9......71")]



def init(matrix):
    for i in range(9):
        for j in range(9):
            if matrix[i][j]==".":
                matrix[i][j]="123456789"


def create_block_by_i(i):
    m,n=i//3,i%3
    return [(m*3+row,n*3+col)for row in range(3) for col in range(3)]
def create_block(row,col):
    m,n=row//3,col//3
    return [(m*3+_row,n*3+_col)for _row in range(3) for _col in range(3)]
def create_row(row):
    return [(row,col) for col in range(9)]
def create_col(col):
    return [(row,col) for row in range(9)]
def basic_broad(matrix,index_list,tar_list):
    """
    在index_list的范围内广播tar_list的影响
    """
    for tar in tar_list:
        for row,col in index_list:
            if len(matrix[row][col])>1:
                matrix[row][col]=matrix[row][col].replace(tar,"")
                if len(matrix[row][col])==1:
                    fresh(matrix,row,col)
            
def fresh(matrix,row,col):
    tar=matrix[row][col]
    basic_broad(matrix,create_row(row),tar)
    basic_broad(matrix,create_col(col),tar)
    basic_broad(matrix,create_block(row,col),tar)



def total_length(matrix):
    total_len=0
    for row in range(9):
        for col in range(9):
            total_len+=len(matrix[row][col])
    return total_len

def is_repeat(matrix,index_list):
    all_num=set()
    for row,col in index_list:
        all_num.add(matrix[row][col])
    if len(all_num)<9:
        return False
    else:
        return True
def is_finish(matrix):
    if total_length(matrix)!=81:
        return False
    for i in range(9):
        if not is_repeat(matrix,create_row(i)):
            return False
        if not is_repeat(matrix,create_col(i)):
            return False
        if not is_repeat(matrix,create_block_by_i(i)):
            return False
    return True


def one_number_stratege(matrix,index_list,block):
    import collections
    num_unsure="123456789"
    for row,col in index_list:
        if len(matrix[row][col])==1:
            num_unsure.replace(matrix[row][col],"")
        num_unsure_position=[[] for _ in range(len(num_unsure))]
        for k in range(len(num_unsure)):
            for row,col in index_list:
                if num_unsure[k] in matrix[row][col]:
                    num_unsure_position[k].append((row,col))
        ###如果位置唯一
        for k in range(len(num_unsure)):
            if len(num_unsure_position[k])==1:
                row_unique,col_unique=num_unsure_position[k][0]
                matrix[row_unique][col_unique]=num_unsure[k]
                fresh(matrix,row_unique,col_unique)
            else:
                ###如果位置有信息
                row_list,col_list=zip(*num_unsure_position[k])
                if block:
                    if len(set(row_list))==1:
                        broad_list=[(row,col) for row,col in create_row(row_list[0]) if col not in col_list]
                        basic_broad(matrix,broad_list,num_unsure[k])
                    if len(set(col_list))==1:
                        broad_list=[(row,col) for row,col in create_col(col_list[0]) if row not in row_list]
                        basic_broad(matrix,broad_list,num_unsure[k])
                else:
                    if len(set(row_list))==1:
                        col_block=[col//3 for col in col_list]
                        if len(set(col_block))==1:
                            broad_list=[row_col for row_col in create_block(row_list[0],col_list[0]) if row_col not in num_unsure_position[k]]
                            basic_broad(matrix,broad_list,num_unsure[k])
                    if len(set(col_list))==1:
                        row_block=[row//3 for row in row_list]
                        if len(set(row_block))==1:
                            broad_list=[row_col for row_col in create_block(row_list[0],col_list[0]) if row_col not in num_unsure_position[k]]
                            basic_broad(matrix,broad_list,num_unsure[k])

                            
                        
def two_number_stratege(matrix,index_list):
    for i in range(9):
        row1,col1=index_list[i]
        if len(matrix[row1][col1])==2:
            for j in range(i+1,9):
                row2,col2=index_list[j]
                if matrix[row2][col2]==matrix[row1][col1]:
                    broad_list=[row_col for row_col in index_list if row_col!=(row1,col1) and row_col!=(row2,col2)]
                    basic_broad(matrix,broad_list,[matrix[row1][col1],matrix[row2][col2]])

def three_number_stratege(matrix,index_list):
    for i in range(9):
        row1,col1=index_list[i]
    if 4>len(matrix[row1][col1])>1:
        for j in range(i+1,9):
            row2,col2=index_list[j]
            if 4>len(matrix[row2][col2])>1:
                for k in range(j+1,9):
                    row3,col3=index_list[k]
                    if 4>len(matrix[row3][col3])>1:
                        union_set=set(matrix[row1][col1]).union(set(matrix[row2][col2])).union(set(matrix[row3][col3]))
                        if len(union_set)==3:
                            broad_list=[row_col for row_col in index_list if row_col!=(row1,col1) and row_col!=(row2,col2) and row_col!=(row3,col3)]
                            basic_broad(matrix,broad_list,[matrix[row1][col1],matrix[row2][col2],matrix[row3][col3]])
def clear_once(matrix):
    for i in range(9):
        ###按行扫描
        one_number_stratege(matrix,create_row(i),block=False)
        two_number_stratege(matrix,create_row(i))
        three_number_stratege(matrix,create_row(i))
        ###按列扫描
        one_number_stratege(matrix,create_col(i),block=False)
        two_number_stratege(matrix,create_col(i))
        three_number_stratege(matrix,create_col(i))
        ###按块扫描
        one_number_stratege(matrix,create_block_by_i(i),block=True)
        two_number_stratege(matrix,create_block_by_i(i))
        three_number_stratege(matrix,create_block_by_i(i))




def guess(matrix,row,col):
    ###注意此处深浅拷贝的区别
    task_copy=[list(x) for x in matrix]
    task_copy[row][col]=task[row][col][0]
    fresh(task_copy,row,col)
    oldsum=700
    while oldsum!=total_length(task_copy):
        oldsum=total_length(task_copy)
        clear_once(task_copy)
    if is_finish(task_copy):
        ##可以优化为全更新
        for i in range(9):
            for j in range(9):
                matrix[i][j]=task_copy[i][j]
        return 0
    else:
        if oldsum==81:
            matrix[row][col]=task[row][col][1]
            fresh(matrix,row,col)
            return 1
        else:
            return 2
def guessanumber(task):
    state=2
    for i in range(9):
        if state!=2:
            break
        for j in range(9):
            if state!=2:
                break
            if len(task[i][j])==2:
                state=guess(task,i,j)

def solve_shudu(matrix):
	init(matrix)
	while not is_finish(matrix):
	    oldsum=800
	    while oldsum!=total_length(matrix):
	        oldsum=total_length(matrix)
	        clear_once(matrix)
	    if oldsum!=81:
	        guessanumber(matrix)        
	print(matrix)
	return matrix
                    