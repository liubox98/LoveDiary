<template>
    <el-scrollbar height="98vh">
        <div class="container">
            <br />
            <el-col :span="24" class="avatar-col">
                <el-divider content-position="right"><el-avatar :style="{ background: '#FF69B4' }" :size="55">
                        {{ this.$store.getters.currentUser }}
                    </el-avatar></el-divider>
            </el-col>
            <br />
            <el-alert :title="`我们 ${formattedElapsedTime}啦啦啦！`" type="success" :closable="false" />
            <!-- <el-alert :title="`我们 ${formattedElapsedTime} 啦啦啦！\t制表符`" type="success" :closable="false" style="white-space: pre-wrap;" /> -->

            <br />
            <el-divider content-position="left"><el-button type="primary" @click="showFormDialog" size="large"><el-icon>
                        <Edit />
                    </el-icon>新增事件</el-button></el-divider>
            <br />
            <el-dialog v-model="formDialogVisible" title="Add" :width="widthVariable">
                <el-form :model="activity" ref="activityForm" label-width="auto">
                    <el-form-item label="活动:" prop="action"
                        :rules="[{ required: true, message: '请输入活动', trigger: 'blur' }]">
                        <el-input v-model="activity.action" placeholder="Enter action" clearable></el-input>
                    </el-form-item>

                    <el-form-item label="描述:" prop="description">
                        <el-input v-model="activity.description" placeholder="Enter description" clearable></el-input>
                    </el-form-item>
                    <el-form-item label="图片:" prop="description">
                        <el-upload @change="handleFileChange" ref="upload" action="/activities" list-type="picture-card"
                            :auto-upload="false" :file-list="selectedFiles" @remove="handleRemove">
                            <el-icon>
                                <Plus />
                            </el-icon>
                            <template #file="{ file }">
                                <div>
                                    <img class="el-upload-list__item-thumbnail" :src="file.url" alt="" />
                                    <span class="el-upload-list__item-actions">
                                        <span class="el-upload-list__item-preview" @click="handlePictureCardPreview(file)">
                                            <el-icon><zoom-in /></el-icon>
                                        </span>
                                        <span v-if="!disabled" class="el-upload-list__item-delete"
                                            @click="handleRemove(file)">
                                            <el-icon>
                                                <Delete />
                                            </el-icon>
                                        </span>
                                    </span>
                                </div>
                            </template>
                        </el-upload>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="submitActivity" :loading="submitting">添加</el-button>
                    </el-form-item>
                </el-form>
            </el-dialog>

            <el-dialog v-model="dialogVisible">
                <img w-full :src="dialogImageUrl" alt="Preview Image" />
            </el-dialog>

            <el-dialog v-model="dialogFormVisible" title="Details">
                <el-form :model="selectedActivity" label-width="auto">
                    <el-form-item>
                        <el-carousel height="150px">
                            <el-carousel-item v-for="item in selectedActivity.image" :key="item.url">
                                <img :src="item.url" alt="carousel-item" style="width: 100%;" />
                            </el-carousel-item>
                        </el-carousel>
                    </el-form-item>
                    <el-form-item>
                        <el-input v-model="selectedActivity.action" disabled />
                    </el-form-item>
                    <el-form-item>
                        <el-input v-model="selectedActivity.description" disabled />
                    </el-form-item>
                    <el-form-item>
                        <el-tag class="ml-2" type="success">{{ formattedCurrentDate(selectedActivity.time) }}</el-tag>
                    </el-form-item>
                </el-form>
            </el-dialog>

            <el-row>
                <el-col v-for="activity in activities" :key="activity._id" :span="6">
                    <el-card :body-style="{ padding: '0px' }" class="activity-card">
                        <img :src="activity.author === 'hanbao' ? hanbaoUrl : baoUrl" class="image" />
                        <div style="padding: 14px">
                            <span>{{ activity.action }}</span>
                            <div class="bottom">
                                <time class="time">{{ formattedCurrentDate(activity.time) }}</time>
                                <div class="button-container">
                                    <el-button class="button" @click="showActivityDetails(activity)">详情</el-button>
                                </div>
                            </div>
                        </div>
                    </el-card>
                </el-col>
                <el-col v-if="activities.length === 0" :span="24">
                    <el-alert title="No activities found" type="info" show-icon :closable="false"></el-alert>
                </el-col>
            </el-row>
        </div>
    </el-scrollbar>
</template>
<script>
export default {
    data() {
        return {
            widthVariable: '33%',
            activity: { action: '', description: '', time: new Date().toISOString() },
            activities: [],
            startTime: new Date('2023-11-01T00:00:00').getTime(),
            elapsedTime: 0,
            disabled: false,
            dialogVisible: false,
            formDialogVisible: false,
            dialogImageUrl: '',
            selectedFiles: [],
            submitting: false,
            selectedActivity: null,
            dialogFormVisible: false,
        };
    },
    computed: {
        baoUrl() {
            return 'https://fuss10.elemecdn.com/a/3f/3302e58f9a181d2509f3dc0fa68b0jpeg.jpeg';
        },
        hanbaoUrl() {
            return 'https://shadow.elemecdn.com/app/element/hamburger.9cf7b091-55e9-11e9-a976-7f4d0b07eef6.png'
        },
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
                this.activities = (await this.$axios.get('/activities')).data;
            } catch (error) {
                console.error('Error fetching activities:', error);
            }
        },
        async submitActivity() {
            if (this.activity.action.length == 0) {
                return;
            }
            try {
                this.submitting = true;
                this.activity.author = this.$store.getters.currentUser
                this.activity.image = this.selectedFiles.map(file => ({
                    name: file.name,
                    url: file.url,
                }));
                await this.$axios.post('/activities', this.activity);
                this.fetchActivities();
                this.clearForm();
            } catch (error) {
                console.error('Error submitting activity:', error);
            } finally {
                this.submitting = false;
            }
        },
        async blobToDataURL(blob) {
            return new Promise((resolve, reject) => {
                const reader = new FileReader();
                reader.onloadend = () => resolve(reader.result);
                reader.onerror = reject;
                reader.readAsDataURL(blob);
            });
        },
        clearForm() {
            this.activity.action = '';
            this.activity.description = '';
            this.activity.image = [];
            this.formDialogVisible = false;
            this.selectedFiles = [];

        },
        updateElapsedTime() {
            setInterval(() => {
                this.elapsedTime = Math.floor((Date.now() - this.startTime) / 1000);
            }, 1000);
        },
        handleFileChange(file, fileList) {
            this.selectedFiles = fileList;
        },
        handleRemove(file) {
            const index = this.selectedFiles.findIndex(selectedFile => selectedFile.uid === file.uid);
            if (index !== -1) {
                this.selectedFiles.splice(index, 1);
            }
        },
        handlePictureCardPreview(file) {
            if (file.url) {
                this.dialogImageUrl = file.url;
                this.dialogVisible = true;
            }
        },
        showFormDialog() {
            this.formDialogVisible = true;
        },
        formattedCurrentDate(time) {
            const date = new Date(time);
            return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(
                date.getHours()
            ).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`;
        },
        showActivityDetails(activity) {
            console.log('activity:', activity)
            this.selectedActivity = activity;
            this.dialogFormVisible = true;
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

.image {
    width: 100%;
    display: block;
}

.bottom {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.button-container {
    margin-left: auto;
}

.time {
    font-size: 12px;
    color: #999;
}

.activity-card {
    margin: 10px 10px 10px 10px;
}

.avatar-col {
    text-align: right;
}
</style>
  