<template>
    <div>
        <van-count-down :time="countdownTime" format="DD 天 HH 时 mm 分 ss 秒" />
    </div>
    <div>
        <van-form @submit="submitActivity">
            <van-field v-model="activity.action" label="Action" placeholder="Enter action" required></van-field>
            <van-field v-model="activity.description" label="Description" placeholder="Enter description"
                required></van-field>
            <van-button type="primary" native-type="submit">Add Activity</van-button>
        </van-form>
        <van-list>
            <van-cell v-for="activity in activities" :key="activity._id">
                {{ activity.action }} - {{ activity.description }} - {{ activity.timestamp }}
            </van-cell>
        </van-list>
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
        };
    },
    computed: {
        countdownTime() {
            const currentTime = new Date().getTime();
            const timeDifference = currentTime - this.startTime;
            return timeDifference > 0 ? timeDifference : 0;
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
            } catch (error) {
                console.error('Error submitting activity:', error);
            }
        },
        clearActivityForm() {
            this.activity.action = '';
            this.activity.description = '';
        },
    },
    mounted() {
        this.fetchActivities();
    },
};
</script>
  