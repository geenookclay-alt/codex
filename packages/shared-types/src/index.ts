export type AssetStatus = 'new' | 'analyzed' | 'planned' | 'produced' | 'uploaded' | 'archived';
export type QueueStatus = 'draft' | 'render_ready' | 'review_ready' | 'upload_ready' | 'scheduled' | 'uploaded' | 'failed';
export interface ChannelProfile { channel_name:string; niche:string; platform:string; language:string; tone:string; preferred_strategy_types:string[]; upload_slots:string[]; banned_patterns:string[]; preferred_title_patterns:string[]; subtitle_style:string; thumbnail_style:string; auto_queue_threshold:number; }
