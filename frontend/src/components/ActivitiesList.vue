<template>
    <div class="container">
        <br />
        <el-row>
            <el-col :span="12">
                <div class="elapsed-time">
                    <span>{{ formattedElapsedTime }}</span>
                </div>
            </el-col>
            <el-col :span="12">
                <el-button type="primary" @click="showFormDialog">Create Activity</el-button>
            </el-col>
        </el-row>
        <br />

        <!-- 弹窗部分 -->
        <el-dialog v-model:visible="formDialogVisible" title="Create Activity">
            <el-form :model="activity" ref="activityForm" label-width="80px">
                <el-form-item label="Action" prop="action">
                    <el-input v-model="activity.action" placeholder="Enter action" clearable></el-input>
                </el-form-item>
                <el-form-item label="Description" prop="description">
                    <el-input v-model="activity.description" placeholder="Enter description" clearable></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="submitActivity">Add Activity</el-button>
                </el-form-item>
            </el-form>
        </el-dialog>

        <el-row>
            <el-col v-for="activity in activities" :key="activity._id" :span="5">
                <el-card :body-style="{ padding: '0px' }" class="activity-card">
                    <img src="https://shadow.elemecdn.com/app/element/hamburger.9cf7b091-55e9-11e9-a976-7f4d0b07eef6.png"
                        class="image" />
                    <div style="padding: 14px">
                        <span>{{ activity.action }} - {{ activity.description }} - {{ activity.timestamp }}</span>
                        <time class="time">{{ currentDate }}</time>
                    </div>
                </el-card>
            </el-col>
            <el-col v-if="activities.length === 0" :span="24">
                <el-alert title="No activities found" type="info" show-icon></el-alert>
            </el-col>
        </el-row>
    </div>
</template>
  
<script>
export default {
    data() {
        return {
            activity: {
                action: '',
                description: '',
            },
            activities: [],
            startTime: new Date('2023-11-01T00:00:00').getTime(),
            elapsedTime: 0,
            formDialogVisible: false,
        };
    },
    computed: {
        formattedElapsedTime() {
            const days = Math.floor(this.elapsedTime / (3600 * 24));
            const hours = Math.floor((this.elapsedTime % (3600 * 24)) / 3600);
            const minutes = Math.floor((this.elapsedTime % 3600) / 60);
            const seconds = this.elapsedTime % 60;

            return `${days} 天 ${hours} 时 ${minutes} 分 ${seconds} 秒`;
        },
    },
    methods: {
        async fetchActivities() {
            try {
                const response = await this.$axios.get('/activities');
                this.activities = response.data;
            } catch (error) {
                console.error('Error fetching activities:', error);
            }
        },
        async submitActivity() {
            try {
                await this.$axios.post('/activities', this.activity);
                this.fetchActivities();
                this.clearActivityForm();
                this.formDialogVisible = false; // 关闭弹窗
            } catch (error) {
                console.error('Error submitting activity:', error);
            }
        },
        clearActivityForm() {
            this.activity.action = '';
            this.activity.description = '';
        },
        updateElapsedTime() {
            setInterval(() => {
                this.elapsedTime = Math.floor((Date.now() - this.startTime) / 1000);
            }, 1000);
        },
        showFormDialog() {
            this.formDialogVisible = true;
        },
    },
    mounted() {
        this.fetchActivities();
        this.updateElapsedTime();
    },
};
</script>
  
<style>
.container {
    width: 50%;
    margin: 0 auto;
}

.elapsed-time {
    display: flex;
    align-items: center;
    font-size: 18px;
}

.elapsed-time i {
    margin-right: 5px;
    font-size: 24px;
    color: #409eff;
}

.time {
    font-size: 12px;
    color: #999;
}

.bottom {
    margin-top: 13px;
    line-height: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.button {
    padding: 0;
    min-height: auto;
}

.image {
    width: 100%;
    display: block;
}

/* 调整卡片之间的间距，增大间距 */
.activity-card {
    margin: 10px 10px 20px 10px;
    /* 从上到下的顺序是：上 右 下 左 */
}
</style>
  