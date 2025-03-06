<template><div class="tool-combination-detail">
    <div class="header">
      <el-page-header @back="goBack" :content="combination?.name || '도구 조합 상세'">
        <template #extra>
          <div class="header-actions" v-if="isOwner">
            <el-button type="primary" @click="editCombination">수정</el-button>
            <el-button type="danger" @click="confirmDelete">삭제</el-button>
          </div>
        </template>
      </el-page-header>
    </div>

    <el-skeleton :loading="loading" animated>
      <template #template>
        <div class="skeleton-content">
          <el-skeleton-item variant="p" style="width: 60%" />
          <el-skeleton-item variant="text" style="width: 80%" />
          <el-skeleton-item variant="h3" style="width: 40%; margin-top: 20px" />
          <el-skeleton-item variant="text" style="width: 100%" v-for="i in 3" :key="i" />
        </div>
      </template>

      <template #default>
        <div v-if="combination" class="combination-content">
          <el-descriptions :column="1" border>
            <el-descriptions-item label="설명">
              {{ combination.description }}
            </el-descriptions-item>
            <el-descriptions-item label="작성자">
              {{ combination.user_id }}
            </el-descriptions-item>
            <el-descriptions-item label="공개 여부">
              <el-tag :type="combination.is_public ? 'success' : 'info'">
                {{ combination.is_public ? '공개' : '비공개' }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="생성일">
              {{ formatDate(combination.created_at) }}
            </el-descriptions-item>
            <el-descriptions-item label="수정일">
              {{ formatDate(combination.updated_at) }}
            </el-descriptions-item>
          </el-descriptions>

          <div class="tools-section">
            <h2>사용된 도구</h2>
            <el-row :gutter="20">
              <el-col 
                :xs="24" 
                :sm="12" 
                :md="8" 
                v-for="toolId in combination.tools" 
                :key="toolId"
              >
                <el-card class="tool-card" shadow="hover">
                  <template #header>
                    <div class="tool-header">
                      <h3>{{ getToolName(toolId) }}</h3>
                    </div>
                  </template>
                  <p>{{ getToolDescription(toolId) }}</p>
                  <div class="tool-actions">
                    <el-button 
                      type="primary" 
                      text 
                      @click="viewToolDetails(toolId)"
                    >
                      자세히 보기
                    </el-button>
                  </div>
                </el-card>
              </el-col>
            </el-row>
          </div>

          <div class="workflow-section">
            <h2>워크플로우</h2>
            <el-timeline>
              <el-timeline-item
                v-for="step in combination.workflow.steps"
                :key="step.order"
                :timestamp="getToolName(step.tool)"
                placement="top"
              >
                <el-card>
                  <h4>Step {{ step.order }}</h4>
                  <p>{{ step.action }}</p>
                </el-card>
              </el-timeline-item>
            </el-timeline>
          </div>
        </div>
      </template>
    </el-skeleton>

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
import { useRouter, useRoute } from 'vue-router';
import { ElMessage } from 'element-plus';
import dayjs from 'dayjs';

export default {
  name: 'ToolCombinationDetailView',
  setup() {
    const store = useStore();
    const router = useRouter();
    const route = useRoute();
    const deleteDialogVisible = ref(false);
    const loading = ref(true);

    const combination = computed(() => store.state.toolCombinations.currentCombination);
    const userId = computed(() => store.state.auth.user?.id);
    const isOwner = computed(() => combination.value?.user_id === userId.value);

    const getToolName = (toolId) => {
      const tool = store.state.tools.tools.find(t => t.id === toolId);
      return tool ? tool.name : '알 수 없는 도구';
    };

    const getToolDescription = (toolId) => {
      const tool = store.state.tools.tools.find(t => t.id === toolId);
      return tool ? tool.description : '';
    };

    const formatDate = (date) => {
      return dayjs(date).format('YYYY-MM-DD HH:mm');
    };

    const goBack = () => {
      router.push('/tools/combinations');
    };

    const editCombination = () => {
      router.push(`/tools/combinations/edit/${combination.value.id}`);
    };

    const viewToolDetails = (toolId) => {
      router.push(`/tools/${toolId}`);
    };

    const confirmDelete = () => {
      deleteDialogVisible.value = true;
    };

    const deleteCombination = async () => {
      try {
        await store.dispatch('toolCombinations/deleteCombination', {
          id: combination.value.id,
          userId: userId.value
        });
        ElMessage.success('도구 조합이 삭제되었습니다.');
        deleteDialogVisible.value = false;
        router.push('/tools/combinations');
      } catch (error) {
        ElMessage.error('도구 조합 삭제 중 오류가 발생했습니다.');
      }
    };

    onMounted(async () => {
      const id = route.params.id;
      try {
        await store.dispatch('toolCombinations/fetchCombination', { id });
      } catch (error) {
        ElMessage.error('도구 조합을 불러오는데 실패했습니다.');
      } finally {
        loading.value = false;
      }
    });

    return {
      combination,
      loading,
      isOwner,
      deleteDialogVisible,
      getToolName,
      getToolDescription,
      formatDate,
      goBack,
      editCombination,
      viewToolDetails,
      confirmDelete,
      deleteCombination
    };
  }
};
</script>

<style scoped>
.tool-combination-detail {
  padding: 20px;
}

.header {
  margin-bottom: 30px;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.combination-content {
  max-width: 1200px;
  margin: 0 auto;
}

.tools-section,
.workflow-section {
  margin-top: 40px;
}

.tools-section h2,
.workflow-section h2 {
  margin-bottom: 20px;
}

.tool-card {
  margin-bottom: 20px;
}

.tool-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.tool-header h3 {
  margin: 0;
}

.tool-actions {
  margin-top: 15px;
  text-align: right;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.skeleton-content {
  padding: 20px;
}
</style>
