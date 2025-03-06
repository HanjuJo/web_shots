<template><div class="tool-combinations">
    <div class="header">
      <h1>AI 도구 조합</h1>
      <router-link 
        to="/tools/combinations/create" 
        class="btn-create"
        v-if="isAuthenticated"
      >
        새 도구 조합 만들기
      </router-link>
    </div>

    <div class="filters">
      <el-radio-group v-model="filter" @change="filterCombinations">
        <el-radio-button label="all">전체</el-radio-button>
        <el-radio-button label="my" v-if="isAuthenticated">내 조합</el-radio-button>
        <el-radio-button label="public">공개</el-radio-button>
      </el-radio-group>
    </div>

    <el-row :gutter="20" class="combinations-grid">
      <el-col 
        :xs="24" 
        :sm="12" 
        :md="8" 
        :lg="6" 
        v-for="combination in filteredCombinations" 
        :key="combination.id"
      >
        <el-card class="combination-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <h3>{{ combination.name }}</h3>
              <el-dropdown v-if="isOwner(combination)" trigger="click">
                <el-button type="text">
                  <i class="el-icon-more"></i>
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item @click="editCombination(combination)">
                      수정
                    </el-dropdown-item>
                    <el-dropdown-item @click="confirmDelete(combination)">
                      삭제
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
          </template>
          
          <div class="combination-content">
            <p class="description">{{ combination.description }}</p>
            <div class="tools-list">
              <h4>사용된 도구:</h4>
              <el-tag 
                v-for="toolId in combination.tools" 
                :key="toolId"
                size="small"
                class="tool-tag"
              >
                {{ getToolName(toolId) }}
              </el-tag>
            </div>
            <div class="workflow">
              <h4>워크플로우:</h4>
              <el-steps direction="vertical" :active="combination.workflow.steps.length">
                <el-step 
                  v-for="step in combination.workflow.steps"
                  :key="step.order"
                  :title="getToolName(step.tool)"
                  :description="step.action"
                />
              </el-steps>
            </div>
          </div>

          <div class="card-footer">
            <el-button 
              type="primary" 
              @click="viewDetails(combination)"
            >
              자세히 보기
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-dialog
      v-model="deleteDialogVisible"
      title="도구 조합 삭제"
      width="30%"
    >
      <span>정말로 이 도구 조합을 삭제하시겠습니까?</span>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="deleteDialogVisible = false">취소</el-button>
          <el-button type="danger" @click="deleteCombination">삭제</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';

export default {
  name: 'ToolCombinationsView',
  setup() {
    const store = useStore();
    const router = useRouter();
    const filter = ref('all');
    const deleteDialogVisible = ref(false);
    const combinationToDelete = ref(null);

    const isAuthenticated = computed(() => store.state.auth.isAuthenticated);
    const userId = computed(() => store.state.auth.user?.id);
    const tools = computed(() => store.state.tools.tools);

    const combinations = computed(() => store.state.toolCombinations.combinations);
    const filteredCombinations = computed(() => {
      switch (filter.value) {
        case 'my':
          return combinations.value.filter(c => c.user_id === userId.value);
        case 'public':
          return combinations.value.filter(c => c.is_public);
        default:
          return combinations.value;
      }
    });

    const getToolName = (toolId) => {
      const tool = tools.value.find(t => t.id === toolId);
      return tool ? tool.name : '알 수 없는 도구';
    };

    const isOwner = (combination) => {
      return combination.user_id === userId.value;
    };

    const filterCombinations = () => {
      // 필터 변경 시 필요한 추가 로직이 있다면 여기에 구현
    };

    const viewDetails = (combination) => {
      router.push(`/tools/combinations/${combination.id}`);
    };

    const editCombination = (combination) => {
      router.push(`/tools/combinations/edit/${combination.id}`);
    };

    const confirmDelete = (combination) => {
      combinationToDelete.value = combination;
      deleteDialogVisible.value = true;
    };

    const deleteCombination = async () => {
      try {
        await store.dispatch('toolCombinations/deleteCombination', {
          id: combinationToDelete.value.id,
          userId: userId.value
        });
        ElMessage.success('도구 조합이 삭제되었습니다.');
        deleteDialogVisible.value = false;
      } catch (error) {
        ElMessage.error('도구 조합 삭제 중 오류가 발생했습니다.');
      }
    };

    onMounted(async () => {
      if (isAuthenticated.value) {
        await store.dispatch('toolCombinations/fetchCombinations', userId.value);
      }
    });

    return {
      filter,
      deleteDialogVisible,
      isAuthenticated,
      filteredCombinations,
      getToolName,
      isOwner,
      filterCombinations,
      viewDetails,
      editCombination,
      confirmDelete,
      deleteCombination
    };
  }
};
</script>

<style scoped>
.tool-combinations {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.btn-create {
  text-decoration: none;
}

.filters {
  margin-bottom: 20px;
}

.combinations-grid {
  margin-top: 20px;
}

.combination-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  margin: 0;
}

.combination-content {
  padding: 10px 0;
}

.description {
  color: #666;
  margin-bottom: 15px;
}

.tools-list {
  margin-bottom: 15px;
}

.tool-tag {
  margin-right: 5px;
  margin-bottom: 5px;
}

.workflow {
  margin-top: 15px;
}

.card-footer {
  text-align: right;
  margin-top: 15px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
