<template><div class="create-tool-combination">
    <div class="header">
      <h1>{{ isEditing ? '도구 조합 수정' : '새 도구 조합 만들기' }}</h1>
    </div>

    <el-form 
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="120px"
      class="combination-form"
    >
      <el-form-item label="이름" prop="name">
        <el-input v-model="form.name" placeholder="도구 조합의 이름을 입력하세요" />
      </el-form-item>

      <el-form-item label="설명" prop="description">
        <el-input
          v-model="form.description"
          type="textarea"
          :rows="3"
          placeholder="도구 조합에 대한 설명을 입력하세요"
        />
      </el-form-item>

      <el-form-item label="도구 선택" prop="tools">
        <el-select
          v-model="form.tools"
          multiple
          placeholder="사용할 도구를 선택하세요"
          style="width: 100%"
        >
          <el-option
            v-for="tool in availableTools"
            :key="tool.id"
            :label="tool.name"
            :value="tool.id"
          >
            <div class="tool-option">
              <span>{{ tool.name }}</span>
              <small>{{ tool.description }}</small>
            </div>
          </el-option>
        </el-select>
      </el-form-item>

      <el-form-item label="워크플로우">
        <div class="workflow-steps">
          <draggable
            v-model="form.workflow.steps"
            handle=".drag-handle"
            item-key="order"
            @end="updateStepOrder"
          >
            <template #item="{ element }">
              <div class="workflow-step">
                <div class="drag-handle">
                  <i class="el-icon-rank"></i>
                </div>
                <el-form-item
                  :prop="'workflow.steps.' + element.order + '.tool'"
                  :rules="{ required: true, message: '도구를 선택해주세요' }"
                >
                  <el-select
                    v-model="element.tool"
                    placeholder="도구 선택"
                    style="width: 200px"
                  >
                    <el-option
                      v-for="tool in form.tools"
                      :key="tool"
                      :label="getToolName(tool)"
                      :value="tool"
                    />
                  </el-select>
                </el-form-item>
                <el-form-item
                  :prop="'workflow.steps.' + element.order + '.action'"
                  :rules="{ required: true, message: '작업을 입력해주세요' }"
                >
                  <el-input
                    v-model="element.action"
                    placeholder="작업 설명"
                    style="width: 300px"
                  />
                </el-form-item>
                <el-button
                  type="danger"
                  icon="el-icon-delete"
                  circle
                  @click="removeStep(element.order)"
                />
              </div>
            </template>
          </draggable>
          <div class="add-step">
            <el-button
              type="primary"
              icon="el-icon-plus"
              @click="addStep"
            >
              단계 추가
            </el-button>
          </div>
        </div>
      </el-form-item>

      <el-form-item label="공개 여부">
        <el-switch
          v-model="form.is_public"
          active-text="공개"
          inactive-text="비공개"
        />
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="submitForm">
          {{ isEditing ? '수정' : '생성' }}
        </el-button>
        <el-button @click="cancel">취소</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useStore } from 'vuex';
import { useRouter, useRoute } from 'vue-router';
import { ElMessage } from 'element-plus';
import draggable from 'vuedraggable';

export default {
  name: 'CreateToolCombinationView',
  components: {
    draggable
  },
  setup() {
    const store = useStore();
    const router = useRouter();
    const route = useRoute();
    const formRef = ref(null);

    const isEditing = computed(() => route.params.id !== undefined);
    const userId = computed(() => store.state.auth.user?.id);
    const availableTools = computed(() => store.state.tools.tools);

    const form = ref({
      name: '',
      description: '',
      tools: [],
      workflow: {
        steps: []
      },
      is_public: true,
      user_id: userId.value
    });

    const rules = {
      name: [
        { required: true, message: '이름을 입력해주세요', trigger: 'blur' },
        { min: 2, max: 50, message: '2-50자 사이로 입력해주세요', trigger: 'blur' }
      ],
      description: [
        { required: true, message: '설명을 입력해주세요', trigger: 'blur' },
        { min: 10, max: 500, message: '10-500자 사이로 입력해주세요', trigger: 'blur' }
      ],
      tools: [
        { required: true, message: '최소 1개의 도구를 선택해주세요', trigger: 'change' },
        { type: 'array', min: 1, message: '최소 1개의 도구를 선택해주세요', trigger: 'change' }
      ]
    };

    const getToolName = (toolId) => {
      const tool = availableTools.value.find(t => t.id === toolId);
      return tool ? tool.name : '알 수 없는 도구';
    };

    const addStep = () => {
      const newOrder = form.value.workflow.steps.length + 1;
      form.value.workflow.steps.push({
        order: newOrder,
        tool: '',
        action: ''
      });
    };

    const removeStep = (order) => {
      form.value.workflow.steps = form.value.workflow.steps
        .filter(step => step.order !== order)
        .map((step, index) => ({ ...step, order: index + 1 }));
    };

    const updateStepOrder = () => {
      form.value.workflow.steps = form.value.workflow.steps
        .map((step, index) => ({ ...step, order: index + 1 }));
    };

    const submitForm = async () => {
      if (!formRef.value) return;

      try {
        await formRef.value.validate();
        
        if (isEditing.value) {
          await store.dispatch('toolCombinations/updateCombination', {
            id: route.params.id,
            combination: form.value
          });
          ElMessage.success('도구 조합이 수정되었습니다.');
        } else {
          await store.dispatch('toolCombinations/createCombination', form.value);
          ElMessage.success('도구 조합이 생성되었습니다.');
        }
        
        router.push('/tools/combinations');
      } catch (error) {
        if (error.message) {
          ElMessage.error(error.message);
        } else {
          ElMessage.error('양식을 올바르게 작성해주세요.');
        }
      }
    };

    const cancel = () => {
      router.push('/tools/combinations');
    };

    onMounted(async () => {
      if (isEditing.value) {
        const id = route.params.id;
        await store.dispatch('toolCombinations/fetchCombination', { id });
        const combination = store.state.toolCombinations.currentCombination;
        if (combination) {
          form.value = { ...combination };
        }
      }
    });

    return {
      formRef,
      form,
      rules,
      isEditing,
      availableTools,
      getToolName,
      addStep,
      removeStep,
      updateStepOrder,
      submitForm,
      cancel
    };
  }
};
</script>

<style scoped>
.create-tool-combination {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.header {
  margin-bottom: 30px;
}

.combination-form {
  background: #fff;
  padding: 20px;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.tool-option {
  display: flex;
  flex-direction: column;
}

.tool-option small {
  color: #999;
  font-size: 12px;
}

.workflow-steps {
  min-height: 50px;
}

.workflow-step {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  background: #f5f7fa;
  border-radius: 4px;
  margin-bottom: 10px;
}

.drag-handle {
  cursor: move;
  padding: 5px;
}

.add-step {
  margin-top: 20px;
}
</style>
