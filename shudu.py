#!/usr/bin/env python
# coding: utf-8

class solve_shudu():
	def __init__(self):
		self.matrix=[]
	def read(self, row_list):
		for row in row_list:
			self.matrix.append(list(row))
	def initialize(self):
	    for row in range(9):
	        for col in range(9):
	            if self.matrix[row][col]==".":
	                self.matrix[row][col]="123456789"
	                self.inverse_broad(self.create_row(row).remove((row,col)),row,col)
	                self.inverse_broad(self.create_col(col).remove((row,col)),row,col)
	                self.inverse_broad(self.create_block(row,col).remove((row,col)),row,col)

	###创造行列对
	def create_block_by_i(self,i):
	    m,n=i//3,i%3
	    return [(m*3+row,n*3+col)for row in range(3) for col in range(3)]
	def create_block(self,row,col):
	    m,n=row//3,col//3
	    return [(m*3+_row,n*3+_col)for _row in range(3) for _col in range(3)]
	def create_row(self,row):
	    return [(row,col) for col in range(9)]
	def create_col(self,col):
	    return [(row,col) for row in range(9)]
	###两个基本的广播方法
	def basic_broad(self,index_list,tar_list):
	    """
	    在index_list的范围内广播tar_list的影响
	    """
	    for tar in tar_list:
	        for row,col in index_list:
	            if len(self.matrix[row][col])>1:
	                self.matrix[row][col]=self.matrix[row][col].replace(tar,"")
	                if len(self.matrix[row][col])==1:
	                    self.fresh(self.matrix,row,col)
	def inverse_broad(self,index_list,row_tar, col_tar):
		"""
		将index_list的影响反向广播给tar_index
		"""
		for row,col in index_list:
			if len(self.matrix[row][col])==1:
				self.matrix[row_tar][col_tar]=self.matrix[row_tar][col_tar].replace(self.matrix[row][col],"")
        if len(self.matrix[row_tar][col_tar])==1:
            self.fresh(self.matrix,row_tar,col_tar)

	###填好一个数之后的更新操作           
	def fresh(self,row,col):
	    tar=self.matrix[row][col]
	    self.basic_broad(self.matrix,self.create_row(row),tar)
	    self.basic_broad(self.matrix,self.create_col(col),tar)
	    self.basic_broad(self.matrix,self.create_block(row,col),tar)

	###计算当前矩阵所有字符数
	def total_length(self):
	    total_len=0
	    for row in range(9):
	        for col in range(9):
	            total_len+=len(self.matrix[row][col])
	    return total_len

	def is_repeat(self,index_list):
	    all_num=set()
	    for row,col in index_list:
	        all_num.add(self.matrix[row][col])
	    if len(all_num)<9:
	        return False
	    else:
	        return True
	def is_finish(self):
	    if total_length(self.matrix)!=81:
	        return False
	    for i in range(9):
	        if not self.is_repeat(self.matrix,self.create_row(i)):
	            return False
	        if not self.is_repeat(self.matrix,self.create_col(i)):
	            return False
	        if not self.is_repeat(self.matrix,self.create_block_by_i(i)):
	            return False
	    return True


	def one_number_stratege(self,index_list,block):
	    import collections
	    num_unsure="123456789"
	    for row,col in index_list:
	        if len(self.matrix[row][col])==1:
	            num_unsure.replace(self.matrix[row][col],"")
	        num_unsure_position=[[] for _ in range(len(num_unsure))]
	        for k in range(len(num_unsure)):
	            for row,col in index_list:
	                if num_unsure[k] in self.matrix[row][col]:
	                    num_unsure_position[k].append((row,col))
	        ###如果位置唯一
	        for k in range(len(num_unsure)):
	            if len(num_unsure_position[k])==1:
	                row_unique,col_unique=num_unsure_position[k][0]
	                self.matrix[row_unique][col_unique]=num_unsure[k]
	                self.fresh(self.matrix,row_unique,col_unique)
	            else:
	                ###如果位置有信息
	                row_list,col_list=zip(*num_unsure_position[k])
	                if block:
	                    if len(set(row_list))==1:
	                        broad_list=[(row,col) for row,col in,self.create_row(row_list[0]) if col not in col_list]
	                        self.basic_broad(self.matrix,broad_list,num_unsure[k])
	                    if len(set(col_list))==1:
	                        broad_list=[(row,col) for row,col in create_col(col_list[0]) if row not in row_list]
	                        self.basic_broad(self.matrix,broad_list,num_unsure[k])
	                else:
	                    if len(set(row_list))==1:
	                        col_block=[col//3 for col in col_list]
	                        if len(set(col_block))==1:
	                            broad_list=[row_col for row_col in create_block(row_list[0],col_list[0]) if row_col not in num_unsure_position[k]]
	                            self.basic_broad(self.matrix,broad_list,num_unsure[k])
	                    if len(set(col_list))==1:
	                        row_block=[row//3 for row in row_list]
	                        if len(set(row_block))==1:
	                            broad_list=[row_col for row_col in create_block(row_list[0],col_list[0]) if row_col not in num_unsure_position[k]]
	                            self.basic_broad(self.matrix,broad_list,num_unsure[k])

	                            
	                        
	def two_number_stratege(self,index_list):
	    for i in range(9):
	        row1,col1=index_list[i]
	        if len(self.matrix[row1][col1])==2:
	            for j in range(i+1,9):
	                row2,col2=index_list[j]
	                if self.matrix[row2][col2]==self.matrix[row1][col1]:
	                    broad_list=[row_col for row_col in index_list if row_col!=(row1,col1) and row_col!=(row2,col2)]
	                    self.basic_broad(self.matrix,broad_list,[self.matrix[row1][col1],self.matrix[row2][col2]])

	def three_number_stratege(self,index_list):
	    for i in range(9):
	        row1,col1=index_list[i]
	    if 4>len(self.matrix[row1][col1])>1:
	        for j in range(i+1,9):
	            row2,col2=index_list[j]
	            if 4>len(self.matrix[row2][col2])>1:
	                for k in range(j+1,9):
	                    row3,col3=index_list[k]
	                    if 4>len(self.matrix[row3][col3])>1:
	                        union_set=set(self.matrix[row1][col1]).union(set(self.matrix[row2][col2])).union(set(self.matrix[row3][col3]))
	                        if len(union_set)==3:
	                            broad_list=[row_col for row_col in index_list if row_col!=(row1,col1) and row_col!=(row2,col2) and row_col!=(row3,col3)]
	                            self.basic_broad(self.matrix,broad_list,[self.matrix[row1][col1],self.matrix[row2][col2],self.matrix[row3][col3]])
	def clear_once(self):
	    for i in range(9):
	        ###按行扫描
	        self.one_number_stratege(self.matrix,self.create_row(i),block=False)
	        self.two_number_stratege(self.matrix,self.create_row(i))
	        self.three_number_stratege(self.matrix,self.create_row(i))
	        ###按列扫描
	        self.one_number_stratege(self.matrix,self.create_col(i),block=False)
	        self.two_number_stratege(self.matrix,self.create_col(i))
	        self.three_number_stratege(self.matrix,self.create_col(i))
	        ###按块扫描
	        self.one_number_stratege(self.matrix,self.create_block_by_i(i),block=True)
	        self.two_number_stratege(self.matrix,self.create_block_by_i(i))
	        self.three_number_stratege(self.matrix,self.create_block_by_i(i))




	def guess(self,row,col):
	    ###注意此处深浅拷贝的区别
	    task_copy=[list(x) for x in self.matrix]
	    task_copy[row][col]=self.matrix[row][col][0]
	    self.fresh(task_copy,row,col)
	    oldsum=700
	    while oldsum!=self.total_length(task_copy):
	        oldsum=self.total_length(task_copy)
	        self.clear_once(task_copy)
	    if self.is_finish(task_copy):
	        ##可以优化为全更新
	        for i in range(9):
	            for j in range(9):
	                self.matrix[i][j]=task_copy[i][j]
	        return 0
	    else:
	        if oldsum==81:
	            self.matrix[row][col]=self.matrix[row][col][1]
	            self.fresh(self.matrix,row,col)
	            return 1
	        else:
	            return 2
	def guessanumber(self):
	    state=2
	    for row in range(9):
	        if state!=2:
	            break
	        for col in range(9):
	            if state!=2:
	                break
	            if len(task[row][col])==2:
	                state=self.guess(row,col)

	def solve_shudu(self):
		self.initialize(self.matrix)
		while not self.is_finish(self.matrix):
		    oldsum=800
		    while oldsum!=self.total_length(self.matrix):
		        oldsum=self.total_length(self.matrix)
		        self.clear_once(self.matrix)
		    if oldsum!=81:
		        self.guessanumber(self.matrix)        
		print(self.matrix)
		return self.matrix
   

if __name__=="__main__":
	matrix=input("input a matrix like [\"123...456\",\"234.....89\",...]")
	if matrix=="demo":
		matrix=[".4..63...",##专家
		      ".8.....26",
		      "...1.....",
		      "1..6..4..",
		      "3.7.....8",
		      "....2..5.",
		      "...7..3..",
		      "..4.5....",
		      "9......71"]
	solution=solve_shudu()
	solution.read(matrix)
	solution.solve_shudu()
                 